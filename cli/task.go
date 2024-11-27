/*
A simple task manager CLI application that allows you to list, add, mark as done, delete tasks, and set reminders for tasks.

Usage:
  task [flags] [command]

Available Commands:
  list        List all tasks
  add         Add a task
  done        Mark a task as done
  delete      Delete a task
  reminder    Set a reminder for a task
  help        Show help
*/

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"time"
)

type Task struct {
	Name   string `json:"name"`
	Status string `json:"status"`
}

func main() {
	flag.String("list", "", "List all tasks")
	flag.String("add", "<task_name>", "Add a task")
	flag.String("done", "<task_number>", "Mark a task as done")
	flag.String("delete", "<task_number>", "Delete a task")
	flag.String("reminder", "<time>", "Set a reminder for a task")
	flag.String("help", "", "Show help")
	flag.Parse()

	args := flag.Args()
	if len(args) == 0 {
		flag.PrintDefaults()
		return
	}

	switch args[0] {
	case "list":
		listTasks()
	case "add":
		if len(args) < 2 {
			fmt.Println("Please provide a task name.")
			return
		}
		addTask(args[1])
	case "done":
		if len(args) < 2 {
			fmt.Println("Please provide the task number to mark as done.")
			return
		}
		markTaskAsDone(args[1])
	case "delete":
		if len(args) < 2 {
			fmt.Println("Please provide the task number to delete.")
			return
		}
		deleteTask(args[1])
	case "reminder":
		if len(args) < 2 {
			fmt.Println("Please provide the reminder time (in minutes).")
			return
		}
		setReminder(args[1])
	case "help":
		flag.PrintDefaults()
	default:
		fmt.Println("Unknown command.")
		flag.PrintDefaults()
	}
}

func listTasks() {
	file, err := os.ReadFile("tasks.json")
	if err != nil {
		if os.IsNotExist(err) {
			fmt.Println("No tasks found.")
			return
		}
		log.Fatal(err)
	}

	var tasks []Task
	err = json.Unmarshal(file, &tasks)
	if err != nil {
		log.Fatal(err)
	}

	if len(tasks) == 0 {
		fmt.Println("No tasks found.")
		return
	}

	for i, task := range tasks {
		fmt.Printf("%d. %s [%s]\n", i+1, task.Name, task.Status)
	}
}

func addTask(taskName string) {
	tasks := getTasks()
	tasks = append(tasks, Task{Name: taskName, Status: "pending"})
	saveTasks(tasks)
	fmt.Println("Task added:", taskName)
}

func markTaskAsDone(taskNumber string) {
	index, err := parseTaskNumber(taskNumber)
	if err != nil {
		log.Fatal(err)
	}

	tasks := getTasks()
	if index < 0 || index >= len(tasks) {
		fmt.Println("Invalid task number.")
		return
	}

	tasks[index].Status = "done"
	saveTasks(tasks)
	fmt.Println("Task marked as done:", tasks[index].Name)
}

func deleteTask(taskNumber string) {
	index, err := parseTaskNumber(taskNumber)
	if err != nil {
		log.Fatal(err)
	}

	tasks := getTasks()
	if index < 0 || index >= len(tasks) {
		fmt.Println("Invalid task number.")
		return
	}

	taskName := tasks[index].Name
	tasks = append(tasks[:index], tasks[index+1:]...)
	saveTasks(tasks)
	fmt.Println("Task deleted:", taskName)
}

func setReminder(timeStr string) {
	duration, err := time.ParseDuration(timeStr + "m")
	if err != nil {
		log.Fatal("Invalid time format:", err)
	}

	fmt.Printf("Reminder set for %v minutes.\n", duration.Minutes())
	time.AfterFunc(duration, func() {
		fmt.Println("Reminder: Time is up!")
	})
}

func getTasks() []Task {
	file, err := os.ReadFile("tasks.json")
	if err != nil {
		if os.IsNotExist(err) {
			return []Task{}
		}
		log.Fatal(err)
	}

	var tasks []Task
	err = json.Unmarshal(file, &tasks)
	if err != nil {
		log.Fatal(err)
	}

	return tasks
}

func saveTasks(tasks []Task) {
	file, err := os.Create("tasks.json")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	err = encoder.Encode(tasks)
	if err != nil {
		log.Fatal(err)
	}
}

func parseTaskNumber(taskNumber string) (int, error) {
	var index int
	_, err := fmt.Sscanf(taskNumber, "%d", &index)
	return index - 1, err
}
