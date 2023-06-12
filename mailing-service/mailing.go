package mailing

import (
	"bytes"
	"context"
	"html/template"
	"net/smtp"
	"os"

	"github.com/gomarkdown/markdown"
	"github.com/gomarkdown/markdown/parser"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func (r *SendEmailsRequest) PostEmails(secret string) error {
	subject := "Subject: " + r.Subject + "!\n"
	mine := "MIME-version: 1.0;\nContent-Type: text/html; charset=\"UTF-8\";\n\n"
	msg := []byte(subject + mine + r.Body)
	addr := "smtp.gmail.com:587"

	auth := smtp.PlainAuth("", r.Sender, secret, "smtp.gmail.com")
	if err := smtp.SendMail(addr, auth, r.Sender, r.To, msg); err != nil {
		return err
	}
	return nil
}

func (r *SendEmailsRequest) FormatEmails(templateFileName string) error {
	extensions := parser.CommonExtensions | parser.AutoHeadingIDs
	parser := parser.NewWithExtensions(extensions)
	md := []byte(r.Body)
	html := markdown.ToHTML(md, parser, nil)
	content := template.HTML(string(html[:]))

	templateData := TemplateData{
		CONTENT: content,
		TITLE:   r.Title,
	}

	t, err := template.ParseFiles(templateFileName)
	if err != nil {
		return err
	}
	buf := new(bytes.Buffer)
	err = t.Execute(buf, templateData)
	if err != nil {
		return err
	}
	r.Body = buf.String()
	return nil
}

func (srv *service) SendEmails(ctx context.Context, req *SendEmailsRequest, mails []string) error {
	if srv.secret == "" {
		return status.Error(codes.Internal, "could not retrieve super secret from environement")
	}

	req.To = mails

	err := req.FormatEmails("mail.html")
	if err != nil {
		currentPath, err := os.Executable()
		if err == nil {
			srv.logger.Error("Formating email error from direcory " + currentPath)
		}
		return status.Error(codes.Internal, err.Error())
	}

	err = req.PostEmails(srv.secret)
	if err != nil {
		return status.Error(codes.Internal, err.Error())
	}
	return nil
}
