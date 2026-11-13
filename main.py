
from dataclasses import dataclass
from datetime import datetime, date
from drafter import *


@dataclass
class Assignment:
    """Represent one college assignment."""
    assignment_id: int
    name: str
    class_name: str
    due_date: str
    priority: str
    completed: bool


@dataclass
class State:
    """Store information used throughout the website."""
    assignments: list[Assignment]
    selected_class: str
    selected_priority: str
    message: str


def valid_date(date_text: str) -> bool:
    """Check whether a date is real and uses YYYY-MM-DD."""
    try:
        parsed = datetime.strptime(date_text, "%Y-%m-%d")
        return parsed.strftime("%Y-%m-%d") == date_text
    except ValueError:
        return False


def is_overdue(assignment: Assignment) -> bool:
    """Check whether an unfinished assignment is overdue."""
    if assignment.completed:
        return False

    due = datetime.strptime(assignment.due_date, "%Y-%m-%d").date()
    return due < date.today()


def navigation() -> list:
    """Create navigation buttons shared by the pages."""
    return [
        Button("Home", "index"),
        Button("Add Assignment", "add_page"),
        Button("All Assignments", "all_assignments"),
        Button("Filter by Class", "filter_page"),
        Button("Priorities", "priority_page")
    ]


def assignment_display(assignment: Assignment) -> list:
    """Create the display for one assignment."""
    if assignment.completed:
        status = "Completed"
    elif is_overdue(assignment):
        status = "Overdue"
    else:
        status = "Incomplete"

    return [
        Header(assignment.name, 3),
        "Class: " + assignment.class_name + "\n",
        "Due: " + assignment.due_date + "\n",
        "Priority: " + assignment.priority + "\n",
        "Status: " + status + "\n"
    ]


def assignment_counts(state: State) -> tuple[int, int, int]:
    """Count total, completed, and overdue assignments."""
    completed = 0
    overdue = 0

    for assignment in state.assignments:
        if assignment.completed:
            completed += 1
        elif is_overdue(assignment):
            overdue += 1

    return len(state.assignments), completed, overdue


@route
def index(state: State) -> Page:
    """Display the home dashboard."""
    total, completed, overdue = assignment_counts(state)
    remaining = total - completed

    return Page(state, [
        Header("College Assignment Tracker"),
        "Stay organized and keep track of your work!\n",
        Header("Your Progress", 2),
        "Total assignments: " + str(total) + "\n",
        "Completed: " + str(completed) + "\n",
        "Remaining: " + str(remaining) + "\n",
        "Overdue: " + str(overdue) + "\n",
        state.message + "\n",
        *navigation()
    ])


@route
def add_page(state: State) -> Page:
    """Display the form for adding an assignment."""
    return Page(state, [
        Header("Add New Assignment"),
        state.message + "\n",
        "Assignment name:",
        TextBox("name"),
        "\nClass name:",
        TextBox("class_name"),
        "\nDue date (YYYY-MM-DD):",
        TextBox("due_date"),
        "\nImportance:",
        SelectBox("priority", ["Low", "Medium", "High"]),
        "\n",
        Button("Save Assignment", "save_assignment"),
        *navigation()
    ])


@route
def save_assignment(
    state: State,
    name: str,
    class_name: str,
    due_date: str,
    priority: str
) -> Page:
    """Validate input and add an assignment."""
    if not name.strip() or not class_name.strip():
        state.message = "Please enter a name and class."
        return add_page(state)

    if not valid_date(due_date):
        state.message = "Please enter a real date using YYYY-MM-DD."
        return add_page(state)

    if priority not in ["Low", "Medium", "High"]:
        state.message = "Please select a valid priority."
        return add_page(state)

    new_id = 1

    for assignment in state.assignments:
        if assignment.assignment_id >= new_id:
            new_id = assignment.assignment_id + 1

    new_assignment = Assignment(
        new_id,
        name.strip(),
        class_name.strip(),
        due_date,
        priority,
        False
    )

    state.assignments.append(new_assignment)
    state.message = "Assignment added successfully!"
    return all_assignments(state)


@route
def all_assignments(state: State) -> Page:
    """Display every assignment and its completion status."""
    content = [
        Header("All Assignments"),
        state.message + "\n"
    ]

    if not state.assignments:
        content.append("You have no assignments yet.\n")

    for assignment in state.assignments:
        content.extend(assignment_display(assignment))

        if not assignment.completed:
            content.append(
                Button(
                    "Mark Completed",
                    "complete_assignment",
                    [
                        Argument(
                            "assignment_id",
                            assignment.assignment_id
                        )
                    ]
                )
            )

        content.append(HorizontalRule())

    content.extend(navigation())
    return Page(state, content)


@route
def complete_assignment(
    state: State,
    assignment_id: int
) -> Page:
    """Mark the selected assignment as completed."""
    state.message = "Assignment not found."

    for assignment in state.assignments:
        if assignment.assignment_id == assignment_id:
            assignment.completed = True
            state.message = "Assignment completed!"
            break

    return all_assignments(state)


@route
def filter_page(state: State) -> Page:
    """Display the class filter form."""
    return Page(state, [
        Header("Filter by Class"),
        "Enter a class name, such as CISC 108:\n",
        TextBox("class_choice", state.selected_class),
        "\n",
        Button("Apply Filter", "apply_filter"),
        *navigation()
    ])


@route
def apply_filter(
    state: State,
    class_choice: str
) -> Page:
    """Save the selected class and show matching assignments."""
    state.selected_class = class_choice.strip()

    content = [
        Header("Assignments for " + state.selected_class)
    ]

    found = False

    for assignment in state.assignments:
        if (
            assignment.class_name.lower()
            == state.selected_class.lower()
        ):
            content.extend(assignment_display(assignment))
            found = True

    if not found:
        content.append("No matching assignments found.\n")

    content.extend(navigation())
    return Page(state, content)


@route
def priority_page(state: State) -> Page:
    """Display incomplete assignments by selected priority."""
    content = [
        Header("Priority Tracker"),
        "Choose which priority to display:\n",
        SelectBox(
            "priority_choice",
            ["All", "High", "Medium", "Low"],
            state.selected_priority
        ),
        "\n",
        Button("Apply Priority", "apply_priority"),
        Header("Unfinished Assignments", 2)
    ]

    found = False

    for level in ["High", "Medium", "Low"]:
        for assignment in state.assignments:
            if not assignment.completed:
                matches = (
                    state.selected_priority == "All"
                    or assignment.priority == state.selected_priority
                )

                if matches and assignment.priority == level:
                    content.extend(assignment_display(assignment))
                    found = True

    if not found:
        content.append("No unfinished assignments found.\n")

    content.extend(navigation())
    return Page(state, content)


@route
def apply_priority(
    state: State,
    priority_choice: str
) -> Page:
    """Update the selected priority filter."""
    state.selected_priority = priority_choice
    state.message = "Priority filter updated."
    return priority_page(state)


# Website settings required for the final project.
if __name__ == "__main__":
    set_website_title("College Assignment Tracker")

    set_site_information(
        "Student Developer",
        "A website that helps college students organize assignments.",
        "",
        "College Assignment Tracker planning documents.",
        []
    )

    start_server(State([], "", "All", ""))