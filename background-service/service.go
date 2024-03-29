package background

import (
	"go.uber.org/zap"
)

type Service interface {
	AddProcess(process *Process) error
	CancelProcess(process *Process) error
}

type service struct {
	logger    *zap.Logger
	processes BackGroundProcesses
}

func NewService(logger *zap.Logger) Service {
	return &service{
		logger: logger,
	}
}
