
"""Unit tests for the College Assignment Tracker."""

import unittest

from main import (
    State,
    Assignment,
    valid_date,
    index,
    add_page,
    save_assignment,
    all_assignments,
    complete_assignment,
    filter_page,
    apply_filter,
    priority_page,
    apply_priority
)


class TestAssignmentTracker(unittest.TestCase):
    """Test assignment data, validation, and website routes."""

    def setUp(self) -> None:
        """Create a fresh State before every test."""
        self.state = State([], "", "All", "")

    def test_valid_date(self) -> None:
        """Check that real dates are accepted."""
        self.assertTrue(valid_date("2026-11-20"))
        self.assertTrue(valid_date("2028-02-29"))

    def test_invalid_date(self) -> None:
        """Check that impossible dates are rejected."""
        self.assertFalse(valid_date("2026-02-30"))
        self.assertFalse(valid_date("2026-13-01"))
        self.assertFalse(valid_date("abcdefghij"))
        self.assertFalse(valid_date("2026-1-5"))
        self.assertFalse(valid_date(""))

    def test_assignment_creation(self) -> None:
        """Check that an Assignment stores information."""
        assignment = Assignment(
            1, "Python Homework", "CISC 108",
            "2026-11-20", "High", False
        )

        self.assertEqual(assignment.name, "Python Homework")
        self.assertEqual(assignment.class_name, "CISC 108")
        self.assertFalse(assignment.completed)

    def test_initial_state(self) -> None:
        """Check the initial State values."""
        self.assertEqual(len(self.state.assignments), 0)
        self.assertEqual(self.state.selected_priority, "All")

    def test_home_route(self) -> None:
        """Check that the home route returns a page."""
        page = index(self.state)
        self.assertIsNotNone(page)

    def test_add_page_route(self) -> None:
        """Check that the assignment form route works."""
        page = add_page(self.state)
        self.assertIsNotNone(page)

    def test_save_assignment(self) -> None:
        """Check that saving adds an assignment."""
        save_assignment(
            self.state,
            "Python Homework",
            "CISC 108",
            "2026-11-20",
            "High"
        )

        self.assertEqual(len(self.state.assignments), 1)
        self.assertEqual(
            self.state.assignments[0].name,
            "Python Homework"
        )
        self.assertFalse(self.state.assignments[0].completed)

    def test_save_invalid_date(self) -> None:
        """Check that an impossible date is rejected."""
        save_assignment(
            self.state,
            "Homework",
            "CISC 108",
            "2026-02-30",
            "High"
        )

        self.assertEqual(len(self.state.assignments), 0)
        self.assertIn("date", self.state.message.lower())

    def test_save_missing_name(self) -> None:
        """Check that a missing assignment name is rejected."""
        save_assignment(
            self.state,
            "",
            "CISC 108",
            "2026-11-20",
            "High"
        )

        self.assertEqual(len(self.state.assignments), 0)

    def test_all_assignments_route(self) -> None:
        """Check that the assignment list page works."""
        page = all_assignments(self.state)
        self.assertIsNotNone(page)

    def test_complete_assignment(self) -> None:
        """Check that only the selected assignment is completed."""
        first = Assignment(
            1, "Homework", "CISC 108",
            "2026-11-20", "High", False
        )
        second = Assignment(
            2, "Essay", "ENGL 110",
            "2026-11-25", "Low", False
        )

        self.state.assignments = [first, second]

        complete_assignment(self.state, 1)

        self.assertTrue(self.state.assignments[0].completed)
        self.assertFalse(self.state.assignments[1].completed)

    def test_filter_page_route(self) -> None:
        """Check that the class filter page works."""
        page = filter_page(self.state)
        self.assertIsNotNone(page)

    def test_apply_filter(self) -> None:
        """Check that the selected class changes."""
        apply_filter(self.state, "CISC 108")

        self.assertEqual(self.state.selected_class, "CISC 108")

    def test_priority_page_route(self) -> None:
        """Check that the priority page works."""
        page = priority_page(self.state)
        self.assertIsNotNone(page)

    def test_apply_priority(self) -> None:
        """Check that the selected priority changes."""
        apply_priority(self.state, "High")

        self.assertEqual(self.state.selected_priority, "High")
        self.assertEqual(
            self.state.message,
            "Priority filter updated."
        )


"""Unit tests for the College Assignment Tracker."""

import unittest

from main import (
    State,
    Assignment,
    valid_date,
    index,
    add_page,
    save_assignment,
    all_assignments,
    complete_assignment,
    filter_page,
    apply_filter,
    priority_page,
    apply_priority
)


class TestAssignmentTracker(unittest.TestCase):
    """Test assignment data, validation, and website routes."""

    def setUp(self) -> None:
        """Create a fresh State before every test."""
        self.state = State([], "", "All", "")

    def test_valid_date(self) -> None:
        """Check that real dates are accepted."""
        self.assertTrue(valid_date("2026-11-20"))
        self.assertTrue(valid_date("2028-02-29"))

    def test_invalid_date(self) -> None:
        """Check that impossible dates are rejected."""
        self.assertFalse(valid_date("2026-02-30"))
        self.assertFalse(valid_date("2026-13-01"))
        self.assertFalse(valid_date("abcdefghij"))
        self.assertFalse(valid_date("2026-1-5"))
        self.assertFalse(valid_date(""))

    def test_assignment_creation(self) -> None:
        """Check that an Assignment stores information."""
        assignment = Assignment(
            1, "Python Homework", "CISC 108",
            "2026-11-20", "High", False
        )

        self.assertEqual(assignment.name, "Python Homework")
        self.assertEqual(assignment.class_name, "CISC 108")
        self.assertFalse(assignment.completed)

    def test_initial_state(self) -> None:
        """Check the initial State values."""
        self.assertEqual(len(self.state.assignments), 0)
        self.assertEqual(self.state.selected_priority, "All")

    def test_home_route(self) -> None:
        """Check that the home route returns a page."""
        page = index(self.state)
        self.assertIsNotNone(page)

    def test_add_page_route(self) -> None:
        """Check that the assignment form route works."""
        page = add_page(self.state)
        self.assertIsNotNone(page)

    def test_save_assignment(self) -> None:
        """Check that saving adds an assignment."""
        save_assignment(
            self.state,
            "Python Homework",
            "CISC 108",
            "2026-11-20",
            "High"
        )

        self.assertEqual(len(self.state.assignments), 1)
        self.assertEqual(
            self.state.assignments[0].name,
            "Python Homework"
        )
        self.assertFalse(self.state.assignments[0].completed)

    def test_save_invalid_date(self) -> None:
        """Check that an impossible date is rejected."""
        save_assignment(
            self.state,
            "Homework",
            "CISC 108",
            "2026-02-30",
            "High"
        )

        self.assertEqual(len(self.state.assignments), 0)
        self.assertIn("date", self.state.message.lower())

    def test_save_missing_name(self) -> None:
        """Check that a missing assignment name is rejected."""
        save_assignment(
            self.state,
            "",
            "CISC 108",
            "2026-11-20",
            "High"
        )

        self.assertEqual(len(self.state.assignments), 0)

    def test_all_assignments_route(self) -> None:
        """Check that the assignment list page works."""
        page = all_assignments(self.state)
        self.assertIsNotNone(page)

    def test_complete_assignment(self) -> None:
        """Check that only the selected assignment is completed."""
        first = Assignment(
            1, "Homework", "CISC 108",
            "2026-11-20", "High", False
        )
        second = Assignment(
            2, "Essay", "ENGL 110",
            "2026-11-25", "Low", False
        )

        self.state.assignments = [first, second]

        complete_assignment(self.state, 1)

        self.assertTrue(self.state.assignments[0].completed)
        self.assertFalse(self.state.assignments[1].completed)

    def test_filter_page_route(self) -> None:
        """Check that the class filter page works."""
        page = filter_page(self.state)
        self.assertIsNotNone(page)

    def test_apply_filter(self) -> None:
        """Check that the selected class changes."""
        apply_filter(self.state, "CISC 108")

        self.assertEqual(self.state.selected_class, "CISC 108")

    def test_priority_page_route(self) -> None:
        """Check that the priority page works."""
        page = priority_page(self.state)
        self.assertIsNotNone(page)

    def test_apply_priority(self) -> None:
        """Check that the selected priority changes."""
        apply_priority(self.state, "High")

        self.assertEqual(self.state.selected_priority, "High")
        self.assertEqual(
            self.state.message,
            "Priority filter updated."
        )


if __name__ == "__main__":
    unittest.main()

