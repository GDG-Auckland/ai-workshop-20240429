
class Item:
    def __init__(self, id, title):
        """
        Initializes a new instance of the Item class.

        Args:
            id (int): The unique identifier for the item.
            title (str): The title of the item.
        """
        self.id = id
        self.title = title
        self.complete = False
    
    def get_id(self):
        """
        Returns the id of the item.

        Returns:
            int: The id of the item.
        """
        return self.id
    
    def get_title(self):
        """
        Returns the title of the item.

        Returns:
            str: The title of the item.
        """
        return self.title
    
    def set_id(self, id):
        """
        Sets the id of the item.

        Args:
            id (int): The new id for the item.
        """
        self.id = id

    def set_title(self, title):
        """
        Sets the title of the item.

        Args:
            title (str): The new title for the item.
        """
        self.title = title

    def get_complete(self):
        """
        Returns the completion status of the item.

        Returns:
            bool: True if the item is complete, False otherwise.
        """
        return self.complete

    def toggle_complete(self):
        """
        Toggles the completion status of the item.
        If the item is complete, it will be marked as incomplete.
        If the item is incomplete, it will be marked as complete.
        """
        self.complete = not self.complete

   