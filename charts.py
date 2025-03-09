import matplotlib.pyplot as plt
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.uix.popup import Popup  # Ensure Popup is imported

def show_expense_chart(savings, total_expenses, balance):
    """Displays a pie chart of expenses and balance inside total savings."""
    
    # Ensure balance is non-negative
    balance = max(balance, 0)

    # Define labels and values
    labels = ["Expenses", "Balance"]
    values = [total_expenses, balance]  # Both are part of savings

    colors = ["red", "blue"]  # Expenses - Red, Balance - Blue

    # Create Pie Chart
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
    ax.set_title("Financial Overview (Inside Savings)")

    # Display Chart in Kivy Popup
    popup = Popup(title="Expense Report", content=FigureCanvasKivyAgg(fig), size_hint=(0.9, 0.9))
    popup.open()
