package mailing

import (
	"html/template"

	"context"

	"go.uber.org/zap"
)

type Service interface {
	SendEmails(ctx context.Context, req *SendEmailsRequest, mails []string) error
}

// type mailingAPI struct {
type service struct {
	logger *zap.Logger
	secret string
}

type SendEmailsRequest struct {
	To      []string
	Sender  string
	Subject string
	Title   string
	Body    string
}

type TemplateData struct {
	CODE    string
	CONTENT template.HTML
	TITLE   string
}

func NewService(logger *zap.Logger, secret string) Service {
	return &service{
		logger: logger,
		secret: secret,
	}
}
