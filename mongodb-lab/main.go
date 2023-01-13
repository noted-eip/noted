package main

import (
	"context"
	"fmt"
	"math/rand"
	"strconv"
	"time"

	"github.com/jaevor/go-nanoid"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type Range struct {
	Min int
	Max int
}

func (r Range) Random() int {
	return r.Min + rand.Intn(r.Max-r.Min)
}

type GenerationOptions struct {
	NumAccounts                   int
	NumGroups                     int
	RangeNumMembersPerGroup       Range
	RangeNumInvitesPerGroup       Range
	RangeNumConversationsPerGroup Range
	RangeNumInvitesLinksPerGroup  Range
}

type GroupMember struct {
	AccountID string    `bson:"accountId"`
	Role      string    `bson:"role"`
	JoinedAt  time.Time `bson:"joinedAt"`
}

type GroupInvite struct {
	SenderAccountID    string    `bson:"senderAccountId"`
	RecipientAccountID string    `bson:"recipientAccountId"`
	CreatedAt          time.Time `bson:"createdAt"`
}

type GroupConversation struct {
	ID        string    `bson:"_id"`
	Name      string    `bson:"name"`
	CreatedAt time.Time `bson:"createdAt"`
}

type GroupInviteLink struct {
	Code               string    `bson:"code"`
	CreatedByAccountID string    `bson:"createdByAccountId"`
	CreatedAt          time.Time `bson:"createdAt"`
}

type Group struct {
	ID            string              `bson:"_id"`
	Name          string              `bson:"name"`
	Description   string              `bson:"description"`
	CreatedAt     time.Time           `bson:"createdAt"`
	ModifiedAt    time.Time           `bson:"modifiedAt"`
	Members       []GroupMember       `bson:"members"`
	Invites       []GroupInvite       `bson:"invites"`
	Conversations []GroupConversation `bson:"conversations"`
	InviteLinks   []GroupInviteLink   `bson:"inviteLinks"`
}

var adjectives = []string{
	"Interesting",
	"Bad",
	"Rich",
	"Pretty",
	"Famous",
	"Curious",
	"Lean",
	"Fancy",
}

var animals = []string{
	"Ducks",
	"Dogs",
	"Giraffes",
	"Elephants",
	"Cats",
	"Mice",
	"Snakes",
	"Fish",
}

var cities = []string{
	"Beijing",
	"Seoul",
	"Daegu",
	"Los Angeles",
	"Paris",
}

func randomAccountID(numAccounts int) string {
	return "a" + strconv.Itoa(rand.Intn(numAccounts))
}

func newRandomSentence() string {
	return adjectives[rand.Intn(len(adjectives))] + " " + animals[rand.Intn(len(animals))] + " from " + cities[rand.Intn(len(cities))]
}

func generateGroupMembers(numAccounts int, numMembers int) []GroupMember {
	members := make([]GroupMember, numMembers)

	for i := 0; i < numMembers; i++ {
		members[i].AccountID = randomAccountID(numAccounts)
		members[i].JoinedAt = time.Now()
		if rand.Intn(10) == 5 || i == 0 {
			members[i].Role = "admin"
		}
	}

	return members
}

func generateGroupInvites(numAccounts int, numInvites int) []GroupInvite {
	invites := make([]GroupInvite, numInvites)

	for i := 0; i < numInvites; i++ {
		invites[i].SenderAccountID = randomAccountID(numAccounts)
		invites[i].RecipientAccountID = randomAccountID(numAccounts)
		invites[i].CreatedAt = time.Now()
	}

	return invites
}

func generateGroupInviteLinks(numAccounts int, numInviteLinks int, newUniqueID func() string) []GroupInviteLink {
	inviteLinks := make([]GroupInviteLink, numInviteLinks)

	for i := 0; i < numInviteLinks; i++ {
		inviteLinks[i].Code = newUniqueID()
		inviteLinks[i].CreatedAt = time.Now()
		inviteLinks[i].CreatedByAccountID = randomAccountID(numAccounts)
	}

	return inviteLinks
}

func generateGroupConversations(numAccounts int, numConversations int, newUniqueID func() string) []GroupConversation {
	conversations := make([]GroupConversation, numConversations)

	for i := 0; i < numConversations; i++ {
		conversations[i].ID = newUniqueID()
		conversations[i].Name = newRandomSentence()
		conversations[i].CreatedAt = time.Now()
	}

	return conversations
}

func generateGroups(coll *mongo.Collection, newUniqueID func() string, opts *GenerationOptions) {
	for i := 0; i < opts.NumGroups; i++ {
		group := Group{
			ID:            newUniqueID(),
			Name:          newRandomSentence(),
			Description:   newRandomSentence(),
			CreatedAt:     time.Now(),
			ModifiedAt:    time.Now(),
			Members:       generateGroupMembers(opts.NumAccounts, opts.RangeNumMembersPerGroup.Random()),
			Invites:       generateGroupInvites(opts.NumAccounts, opts.RangeNumInvitesPerGroup.Random()),
			InviteLinks:   generateGroupInviteLinks(opts.NumAccounts, opts.RangeNumInvitesLinksPerGroup.Random(), newUniqueID),
			Conversations: generateGroupConversations(opts.NumAccounts, opts.RangeNumConversationsPerGroup.Random(), newUniqueID),
		}
		coll.InsertOne(context.TODO(), &group)
		fmt.Printf("'%6d' out of '%6d' groups created.\r", i, opts.NumGroups)
	}
}

func main() {
	client, err := mongo.Connect(context.Background(), options.Client().ApplyURI("mongodb://localhost:27017"))
	if err != nil {
		panic(err.Error())
	}

	db := client.Database("mongodb-lab")

	groupsColl := db.Collection("groups")

	newCanonicID, err := nanoid.Standard(21)
	if err != nil {
		panic(err.Error())
	}

	generateGroups(groupsColl, newCanonicID, &GenerationOptions{
		NumAccounts:                   5000,
		NumGroups:                     30000,
		RangeNumMembersPerGroup:       Range{Min: 1, Max: 50},
		RangeNumInvitesPerGroup:       Range{Min: 0, Max: 50},
		RangeNumInvitesLinksPerGroup:  Range{Min: 0, Max: 50},
		RangeNumConversationsPerGroup: Range{Min: 1, Max: 10},
	})
}
