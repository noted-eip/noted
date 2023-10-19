package background

import (
	"errors"
	"strconv"
	"time"

	"github.com/bep/debounce"
	"go.uber.org/zap"
)

// Add a process to the queue which is going to exec a function in X time
func (srv *service) AddProcess(process *Process) error {
	// Check for illegal processes
	if process.Identifier == nil && process.RepeatProcess {
		srv.logger.Error("You can't repeat a process with a nil indentifier, the process could never stop")
		return errors.New("process cannot repeat and have a nil identifier")
	}

	// Cancel the process of the same identifier
	if process.CancelProcessOnSameIdentifier {
		err := srv.CancelProcess(process)
		if err != nil {
			return err
		}
	}
	// Add a process to the list & launch the debounce fct
	lastIndex := len(srv.processes)
	process.debounced = debounce.New(time.Duration(process.SecondsToDebounce) * time.Second)
	srv.processes = append(srv.processes, *process)
	srv.debounceLogic(&srv.processes[lastIndex], process.Identifier)
	return nil
}

// Cancel a process by his identifier
func (srv *service) CancelProcess(process *Process) error {
	if process.Identifier == nil {
		srv.logger.Error("Cannot cancel background process if the identifier is nil")
		return errors.New("identifier cannot be nil")
	}

	for index := 0; index < len(srv.processes); index++ {
		srv.mut.Lock()
		if srv.processes[index].Identifier == process.Identifier {
			// TODO cancel the goroutine by srv.processes.task
			go srv.processes[index].debounced(func() {})
			srv.processes = srv.remove(srv.processes, index)
			index--
		}
		srv.mut.Unlock()
	}
	return nil
}

func (srv *service) debounceLogic(process *Process, id interface{}) {
	logic := func() {

		// Get process ID (naive look-up)
		index := -1
		srv.mut.Lock()
		for i := 0; i < len(srv.processes); i++ {
			if srv.processes[i].Identifier == process.Identifier {
				index = i
				break
			}
		}
		if index == -1 {
			srv.logger.Error("no go routine with this identifier")
			return
		}
		srv.mut.Unlock()

		err := process.CallBackFct()
		if err != nil {
			srv.logger.Error("error in Lambda function in backgroundProcess for task : "+strconv.Itoa(int(srv.processes[index].task)), zap.Error(err))
			return
		}
		if process.RepeatProcess {
			srv.debounceLogic(process, id)
		} else {
			srv.processes = srv.remove(srv.processes, index)
		}
	}
	go process.debounced(logic)
}

func (srv *service) remove(slice []Process, idx int) []Process {
	srv.mut.Lock()
	defer srv.mut.Unlock()
	res := append(slice[:idx], slice[idx+1:]...)
	return res
}
