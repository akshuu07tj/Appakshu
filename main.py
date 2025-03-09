from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle

from database import add_expense, create_db, get_totals, reset_expenses
from charts import show_expense_chart


class ExpenseTrackerApp(App):
    def build(self):
        self.savings = 0
        self.total_expenses = 0
        self.balance = 0

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Set Even Darker Green Background
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Even Darker Green Background
            self.rect = Rectangle(size=layout.size, pos=layout.pos)

        layout.bind(size=self._update_rect, pos=self._update_rect)

        # Title
        title_label = Label(text=" Expense Tracker", font_size=28, bold=True, color=(1, 1, 1, 1))
        layout.add_widget(title_label)

        # Savings, Expenses, and Balance Labels
        self.savings_label = Label(text=f"Savings: ₹{self.savings}", font_size=20, color=(0, 1, 0, 1))
        layout.add_widget(self.savings_label)

        self.expense_label = Label(text=f"Total Expenses: ₹{self.total_expenses}", font_size=20, color=(1, 0, 0, 1))
        layout.add_widget(self.expense_label)

        self.balance_label = Label(text=f"Balance: ₹{self.balance}", font_size=20, color=(1, 1, 0, 1))
        layout.add_widget(self.balance_label)

        # Styled Buttons
        buttons = [
            ("Set Savings", self.set_savings_popup),
            ("Add Expense", self.show_add_expense_popup),
            ("📊 View Reports", self.view_chart),
            ("🔄 Reset", self.reset_fields),
        ]

        for btn_text, btn_function in buttons:
            button = Button(text=btn_text, size_hint=(1, 0.15), font_size=18, background_color=(0.2, 0.6, 1, 1))
            button.bind(on_press=btn_function)
            layout.add_widget(button)

        # Footer with Name and ID
        footer_label = Label(
            text="Tamilarasu V| 2021wa86049", font_size=14, italic=True, color=(1, 1, 1, 0.7)
        )
        layout.add_widget(footer_label)

        self.update_totals()
        return layout

    def _update_rect(self, instance, value):
        """Update the background when resizing the window."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def set_savings_popup(self, instance):
        """Popup to enter savings amount."""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.savings_input = TextInput(hint_text="Enter total savings", multiline=False)
        popup_layout.add_widget(self.savings_input)

        submit_btn = Button(text="Save")
        submit_btn.bind(on_press=self.set_savings)
        popup_layout.add_widget(submit_btn)

        self.savings_popup = Popup(title="Enter Savings", content=popup_layout, size_hint=(0.8, 0.5))
        self.savings_popup.open()

    def set_savings(self, instance):
        """Sets the savings amount and updates the UI."""
        self.savings = float(self.savings_input.text) if self.savings_input.text else 0
        self.update_totals()
        self.savings_popup.dismiss()

    def show_add_expense_popup(self, instance):
        """Popup to enter expense details with a dropdown for payment method."""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.amount_input = TextInput(hint_text="Enter amount", multiline=False)
        popup_layout.add_widget(self.amount_input)

        self.category_input = TextInput(hint_text="Enter category (Food, Travel, etc.)", multiline=False)
        popup_layout.add_widget(self.category_input)

        # Dropdown for Payment Method
        self.payment_method_spinner = Spinner(
            text="Select Payment Method",
            values=("Online Transaction", "Hand to Hand"),
            size_hint=(1, None),
            height=44
        )
        popup_layout.add_widget(self.payment_method_spinner)

        submit_btn = Button(text="Add Expense")
        submit_btn.bind(on_press=self.add_expense)
        popup_layout.add_widget(submit_btn)

        self.popup = Popup(title="Add Expense", content=popup_layout, size_hint=(0.8, 0.5))
        self.popup.open()

    def add_expense(self, instance):
        """Adds an expense to the database and updates the UI."""
        try:
            amount = float(self.amount_input.text) if self.amount_input.text else 0
            category = self.category_input.text
            payment_method = self.payment_method_spinner.text  # Get selected value

            if amount and category and payment_method != "Select Payment Method":
                add_expense(amount, category, payment_method)
                self.update_totals()
                self.popup.dismiss()
        except ValueError:
            pass  # Ignore if input is invalid

    def update_totals(self):
        """Updates expense and balance values in the UI."""
        self.total_expenses = get_totals()
        self.balance = self.savings - self.total_expenses

        self.savings_label.text = f"Savings: ₹{self.savings}"
        self.expense_label.text = f"Total Expenses: ₹{self.total_expenses}"
        self.balance_label.text = f"Balance: ₹{self.balance}"

    def view_chart(self, instance):
        """Displays the expense chart."""
        show_expense_chart(self.savings, self.total_expenses, self.balance)

    def reset_fields(self, instance):
        """Resets all values and clears expense history."""
        reset_expenses()

        # Reset values
        self.savings = 0
        self.total_expenses = 0
        self.balance = 0

        # Update UI labels
        self.update_totals()


if __name__ == "__main__":
    create_db()  # Initialize database
    ExpenseTrackerApp().run()
