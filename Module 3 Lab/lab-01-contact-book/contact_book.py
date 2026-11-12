"""Manage contacts stored as a list of dictionaries."""

from typing import TypeAlias

Contact: TypeAlias = dict[str, str]


def find_contact(contacts: list[Contact], name: str) -> Contact | None:
    """Return the contact whose name matches, ignoring letter case."""
    normalized_name = name.strip().casefold()
    return next(
        (contact for contact in contacts if contact["name"].casefold() == normalized_name),
        None,
    )


def read_required(prompt: str) -> str:
    """Read a non-empty value from the user."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This value cannot be empty.")


def add_contact(contacts: list[Contact]) -> None:
    """Read and add a contact when its name is unique."""
    name = read_required("Enter name: ")
    if find_contact(contacts, name):
        print("A contact with this name already exists.")
        return

    contacts.append(
        {
            "name": name,
            "phone": read_required("Enter phone number: "),
            "email": read_required("Enter email address: "),
        }
    )
    print("Contact added successfully.")


def display_contact(contact: Contact) -> None:
    """Display one contact in a readable format."""
    print(f"Name: {contact['name']}")
    print(f"Phone: {contact['phone']}")
    print(f"Email: {contact['email']}")


def search_contact(contacts: list[Contact]) -> None:
    """Find and display a contact by name."""
    contact = find_contact(contacts, input("Enter name to search: "))
    if contact:
        display_contact(contact)
    else:
        print("Contact not found.")


def update_contact(contacts: list[Contact]) -> None:
    """Update a contact while allowing unchanged fields."""
    contact = find_contact(contacts, input("Enter name to update: "))
    if not contact:
        print("Contact not found.")
        return

    phone = input(f"New phone [{contact['phone']}]: ").strip()
    email = input(f"New email [{contact['email']}]: ").strip()
    if phone:
        contact["phone"] = phone
    if email:
        contact["email"] = email
    print("Contact updated successfully.")


def delete_contact(contacts: list[Contact]) -> None:
    """Delete a contact by name."""
    contact = find_contact(contacts, input("Enter name to delete: "))
    if not contact:
        print("Contact not found.")
        return

    contacts.remove(contact)
    print("Contact deleted successfully.")


def display_all(contacts: list[Contact]) -> None:
    """Display every contact alphabetically."""
    if not contacts:
        print("The contact book is empty.")
        return

    print("\n========== CONTACTS ==========")
    for index, contact in enumerate(
        sorted(contacts, key=lambda item: item["name"].casefold()), start=1
    ):
        print(f"\nContact {index}")
        display_contact(contact)


def main() -> None:
    """Run the contact book menu."""
    contacts: list[Contact] = []
    actions = {
        "1": add_contact,
        "2": search_contact,
        "3": update_contact,
        "4": delete_contact,
        "5": display_all,
    }

    while True:
        print("\n========== CONTACT BOOK ==========")
        print("1. Add contact")
        print("2. Search contact")
        print("3. Update contact")
        print("4. Delete contact")
        print("5. Display all contacts")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "6":
            print("Contact book closed.")
            break
        action = actions.get(choice)
        if action:
            action(contacts)
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
