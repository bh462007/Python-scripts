class Task:
    def __init__(self, title, description, status):
        self.title=title
        self.description=description
        self.status=status
    def mark_completed(self):
        self.status=True
        return f"Task {self.title} is marked as completed"
    
    def display_task(self):
        status_text="Completed" if self.status else "Pending"
        return f"Title: {self.title} | Description: {self.description}"

task1=Task("cleaning", "cleaning and organizing the room",False)
task2=Task("working", "working on a project", False)

print(f"==========Tasks==========")
print(task1.display_task())
print(task2.display_task())


print("\n++++++++++Task after completion++++++++++")
print(task1.mark_completed())
print(task1.display_task())