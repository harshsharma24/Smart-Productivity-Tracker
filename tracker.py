import streamlit as st
import json
from azure.storage.blob import BlobClient


def add_task(task):
    if not task.strip():
        return False

    if task:
        id=st.session_state.tasks[-1]['id'] if st.session_state.tasks else 0
        st.session_state.tasks.append({"id": id+1, "task":task.strip(), "done": False})

    return True

def mark_task(id):
    for i , work in enumerate(st.session_state.tasks):
        if (work['id']) == id:
            st.session_state.tasks.pop((i))
            return True
    return False


def show_tasks_ui():
    st.subheader="Tasks"

    top_col1, top_col2 = st.columns([0.6,0.4])
    
    with top_col2:
        tasks_json= json.dumps(st.session_state.tasks, indent=2)

        st.download_button(
            label="📥 Download Tasks as JSON",
            data=tasks_json,
            file_name="my_tasks.json",
            mime="application/json"
        )
    

    upload_to_blob_storage(tasks_json, "my_tasks.json")


    with top_col1:
        if not st.session_state.tasks:
            return
        
        total_tasks=len(st.session_state.tasks)
        completed_tasks= sum(1 for task in st.session_state.tasks if task["done"])
        pending_tasks= total_tasks - completed_tasks

        # Display Summary
        st.markdown(f"**Total**: {total_tasks} | **Completed**: {completed_tasks} | **Total**: {pending_tasks} ")
        st.markdown("---")
        filter_option=st.selectbox("Filter tasks by: ", ["All","Pending", "Completed"])

        # Filter according to condition
        if filter_option =="Pending":
            filtered_tasks= [task for task in st.session_state.tasks if not task["done"]]
        elif filter_option =="Completed":
            filtered_tasks= [task for task in st.session_state.tasks if task["done"]]
        else:
            filtered_tasks= st.session_state.tasks

        if not filtered_tasks:
            st.info("No tasks match the selected filter.")
            return


        for i, task in enumerate(st.session_state.tasks):
            if task not in filtered_tasks:
                continue

            col1, col2 = st.columns([0.85, 0.5])
            with col1:
                st.markdown(f"**{task['id']}** {task['task']}")
            with col2:
                checked = st.checkbox("Done", key=f"done_{task['id']}_{i}", value=task['done'])
                st.session_state.tasks[i]['done'] = checked


    if "tasks" not in st.session_state:
        st.session_state.tasks=[]

def add_task_ui():
    with st.form("add_task_form"):
        task= st.text_input("Add task Details")
        submitted= st.form_submit_button("Add Task")
        if submitted:
            success=add_task(task)
            if success:
                st.success(f"Added task to list {task}")
            else:
                st.error("Task cannot be empty")

def delete_task_ui():
    with st.form("delete_task_form"):
        delete_choice= (st.text_input(" Enter Id which one to delete: "))
        submitted= st.form_submit_button("Delete Task")
        if submitted:
            if delete_choice.isdigit(): 
                delete_choice= int(delete_choice)
                success=mark_task(delete_choice)
                if success:
                    st.success("Task Deleted")
                else:
                    st.error("Task ID not found")
            else:
                st.error("Please enter a valid numeric ID")

def upload_to_blob_storage(file_data, file_name):
    try:
        sas_token = "sv=2024-11-04&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2025-07-24T14:49:44Z&st=2025-07-24T06:34:44Z&spr=https&sig=PDXW6RCPtB%2Br2P62h%2FErdMX3erx4dVyJMywBYtenMI0%3D"
        account_name = "smartproductivity"
        container_name = "todo"

        blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{file_name}?{sas_token}"

        blob_client = BlobClient.from_blob_url(blob_url)
        blob_client.upload_blob(file_data, overwrite=True)

        st.success(f"✅ File uploaded to Azure Blob: {file_name}")
    except Exception as e:
        st.error(f"❌ Upload failed: {e}")

def main():    
    st.title("Smart Productivity Tracker")

    uploaded_file=st.file_uploader("📤 Upload a tasks file (.json)", type="json")

    if uploaded_file and "tasks_loaded_from_file" not in st.session_state:
        try:
            uploaded_tasks=json.load(uploaded_file)

            if isinstance(uploaded_tasks,list):
                #check existing Ids
                existing_ids={task['id'] for task in st.session_state.tasks}
                next_id=max(existing_ids, default=0)+1

                for task in uploaded_tasks:
                    if task['id'] in existing_ids:
                        continue
                
                    task['id'] = next_id
                    st.session_state.tasks.append(task)

                st.success("Tasks Loaded Successfully")
            else:
                st.error("Invalid File Format")
        except Exception as e:
            st.error(f"Error loading file: {e}")

    choice = st.radio("Choose an Option:", ["Add Task", "Show all Tasks", "Delete Task"])

    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    if choice == "Add Task":
        add_task_ui()
    elif choice == "Show all Tasks":
        show_tasks_ui()
    elif choice == "Delete Task":
        delete_task_ui()

if __name__ == "__main__":
    main()

