package background

import (
	"sync"

	"go.uber.org/zap"
)

type Service interface {
	AddProcess(process *Process) error
	CancelProcess(process *Process) error
}

type service struct {
	mut       sync.Mutex
	logger    *zap.Logger
	processes BackGroundProcesses
}

func NewService(logger *zap.Logger) Service {
	return &service{
		logger: logger,
	}
}
