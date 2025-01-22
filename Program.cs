using System;
using System.Collections.Generic;
using System.IO;

namespace ExpenseTracker
{
    class Program
    {
        static string filePath = "expenses.txt";

        static void Main(string[] args)
        {
            Dictionary<string, decimal> expenses = LoadExpensesFromFile();
            bool running = true;

            while (running)
            {
                Console.WriteLine("\nExpense Tracker:");
                Console.WriteLine("1. Add an Expense");
                Console.WriteLine("2. Remove an Expense");
                Console.WriteLine("3. View Saved Expenses");
                Console.WriteLine("4. Calculate Total Monthly Expenses");
                Console.WriteLine("5. Search for an Expense");
                Console.WriteLine("6. Export Expenses to CSV");
                Console.WriteLine("7. Clear All Expenses");
                Console.WriteLine("8. Exit");
                Console.Write("Choose an option: ");

                string choice = Console.ReadLine();

                switch (choice)
                {
                    case "1":
                        AddExpense(expenses);
                        break;
                    case "2":
                        RemoveExpense(expenses);
                        break;
                    case "3":
                        ViewExpenses(expenses);
                        break;
                    case "4":
                        CalculateTotalExpenses(expenses);
                        break;
                    case "5":
                        SearchExpense(expenses);
                        break;
                    case "6":
                        ExportExpensesToCSV(expenses);
                        break;
                    case "7":
                        ClearAllExpenses(expenses);
                        break;
                    case "8":
                        running = false;
                        SaveExpensesToFile(expenses);
                        Console.WriteLine("Goodbye!");
                        break;
                    default:
                        Console.WriteLine("Invalid choice. Please try again.");
                        break;
                }
            }
        }

        static void AddExpense(Dictionary<string, decimal> expenses)
        {
            Console.Write("Enter the name of the expense: ");
            string name = Console.ReadLine();

            Console.Write("Enter the monthly price of the expense: ");
            if (decimal.TryParse(Console.ReadLine(), out decimal price))
            {
                if (expenses.ContainsKey(name))
                {
                    Console.WriteLine("Expense already exists. Updating the price.");
                }
                expenses[name] = price;
                Console.WriteLine("Expense added/updated successfully.");
                SaveExpensesToFile(expenses);
            }
            else
            {
                Console.WriteLine("Invalid price. Please enter a valid number.");
            }
        }

        static void RemoveExpense(Dictionary<string, decimal> expenses)
        {
            Console.Write("Enter the name of the expense to remove: ");
            string name = Console.ReadLine();

            if (expenses.Remove(name))
            {
                Console.WriteLine("Expense removed successfully.");
                SaveExpensesToFile(expenses);
            }
            else
            {
                Console.WriteLine("Expense not found.");
            }
        }

        static void ViewExpenses(Dictionary<string, decimal> expenses)
        {
            expenses = LoadExpensesFromFile(); // Reload from file

            if (expenses.Count == 0)
            {
                Console.WriteLine("No expenses recorded.");
                return;
            }

            Console.WriteLine("\nSaved Expenses:");
            foreach (var expense in expenses)
            {
                Console.WriteLine($"{expense.Key}: ${expense.Value:F2}");
            }
        }

        static void CalculateTotalExpenses(Dictionary<string, decimal> expenses)
        {
            decimal total = 0;

            foreach (var expense in expenses.Values)
            {
                total += expense;
            }

            Console.WriteLine($"\nTotal Monthly Expenses: ${total:F2}");
        }

        static void SearchExpense(Dictionary<string, decimal> expenses)
        {
            Console.Write("Enter the name of the expense to search: ");
            string name = Console.ReadLine();

            if (expenses.TryGetValue(name, out decimal price))
            {
                Console.WriteLine($"Found: {name} costs ${price:F2}");
            }
            else
            {
                Console.WriteLine("Expense not found.");
            }
        }

        static void ExportExpensesToCSV(Dictionary<string, decimal> expenses)
        {
            string csvFilePath = "expenses.csv";

            using (StreamWriter writer = new StreamWriter(csvFilePath))
            {
                writer.WriteLine("Name,Price");
                foreach (var expense in expenses)
                {
                    writer.WriteLine($"{expense.Key},{expense.Value}");
                }
            }

            Console.WriteLine($"Expenses exported to {csvFilePath} successfully.");
        }

        static void ClearAllExpenses(Dictionary<string, decimal> expenses)
        {
            Console.Write("Are you sure you want to clear all expenses? (yes/no): ");
            string confirmation = Console.ReadLine().ToLower();

            if (confirmation == "yes")
            {
                expenses.Clear();
                SaveExpensesToFile(expenses);
                Console.WriteLine("All expenses have been cleared.");
            }
            else
            {
                Console.WriteLine("Operation canceled.");
            }
        }

        static void SaveExpensesToFile(Dictionary<string, decimal> expenses)
        {
            using (StreamWriter writer = new StreamWriter(filePath))
            {
                foreach (var expense in expenses)
                {
                    writer.WriteLine($"{expense.Key}|{expense.Value}");
                }
            }
        }

        static Dictionary<string, decimal> LoadExpensesFromFile()
        {
            Dictionary<string, decimal> expenses = new Dictionary<string, decimal>();

            if (File.Exists(filePath))
            {
                string[] lines = File.ReadAllLines(filePath);
                foreach (string line in lines)
                {
                    string[] parts = line.Split('|');
                    if (parts.Length == 2 && decimal.TryParse(parts[1], out decimal price))
                    {
                        expenses[parts[0]] = price;
                    }
                }
            }

            return expenses;
        }
    }
}
