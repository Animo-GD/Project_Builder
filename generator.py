import os
import json
import argparse
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from typing import Dict, Any

class ProjectGenerator:
    @staticmethod
    def create_from_json(json_path: str, target_dir: str):
        """Create project structure from JSON file"""
        with open(json_path) as f:
            structure = json.load(f)
        ProjectGenerator.create_structure(target_dir, structure)
    
    @staticmethod
    def create_structure(base_dir: str, structure: Dict[str, Any]):
        """Create project structure from dictionary"""
        base_path = Path(base_dir)
        
        def _create(base: Path, content: Any):
            if isinstance(content, dict):  # Directory
                for name, subcontent in content.items():
                    path = base / name
                    if isinstance(subcontent, dict) or subcontent is None:
                        path.mkdir(parents=True, exist_ok=True)
                        print(f"Created directory: {path}")
                        _create(path, subcontent)
                    else:  # File with content
                        with open(path, 'w') as f:
                            f.write(str(subcontent))
                        print(f"Created file: {path}")
            elif content is not None:  # Root level file
                path = base / content
                path.touch()
                print(f"Created file: {path}")
        
        _create(base_path, structure)
        print(f"\nProject structure created successfully at {base_path}")

class ProjectDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Structure Designer")
        self.root.geometry("1000x700")
        
        self.project_structure = {}
        self.current_path = []
        
        self.setup_ui()
        self.load_sample_structure()
        
    def setup_ui(self):
        # Main frames
        control_frame = Frame(self.root, padx=10, pady=10, width=300)
        control_frame.pack(side=LEFT, fill=Y)
        
        self.tree_frame = Frame(self.root, padx=10, pady=10)
        self.tree_frame.pack(side=RIGHT, expand=True, fill=BOTH)
        
        # Control panel
        Label(control_frame, text="Project Designer", font=('Arial', 14)).pack(pady=10)
        
        Button(control_frame, text="Load JSON", command=self.load_json).pack(fill=X, pady=5)
        Button(control_frame, text="Save JSON", command=self.save_json).pack(fill=X, pady=5)
        Button(control_frame, text="Generate Project", command=self.generate_project).pack(fill=X, pady=20)
        
        # Structure display
        self.tree = ttk.Treeview(self.tree_frame)
        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        # Status bar
        self.status = Label(self.root, text="Ready", bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)
        
    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path) as f:
                    self.project_structure = json.load(f)
                self.update_tree_view()
                self.status.config(text=f"Loaded structure from: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load JSON:\n{str(e)}")
    
    def save_json(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(self.project_structure, f, indent=4)
            self.status.config(text=f"Structure saved to: {file_path}")
    
    def generate_project(self):
        target_dir = filedialog.askdirectory()
        if target_dir:
            try:
                ProjectGenerator.create_structure(target_dir, self.project_structure)
                messagebox.showinfo("Success", f"Project generated at:\n{target_dir}")
                self.status.config(text=f"Project created at: {target_dir}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create project:\n{str(e)}")
    
    def update_tree_view(self):
        self.tree.delete(*self.tree.get_children())
        self._add_tree_node("", self.project_structure)
    
    def _add_tree_node(self, parent, structure):
        if isinstance(structure, dict):
            for name, content in structure.items():
                if isinstance(content, dict):
                    node = self.tree.insert(parent, "end", text=f"📁 {name}", open=True)
                    self._add_tree_node(node, content)
                else:
                    self.tree.insert(parent, "end", text=f"📄 {name}")
    
    def load_sample_structure(self):
        """Load the sample book_recommender structure"""
        self.project_structure = {
            "book_recommender": {
                "app": {
                    "__init__.py": "",
                    "main.py": (
                        "# FastAPI app setup\n"
                        "from fastapi import FastAPI\n"
                        "from .routes import router\n\n"
                        "app = FastAPI()\n"
                        "app.include_router(router)\n\n"
                        "@app.get('/')\n"
                        "def read_root():\n"
                        "    return {'message': 'Welcome to Book Recommender API'}"
                    ),
                    "routes.py": (
                        "# API endpoints\n"
                        "from fastapi import APIRouter\n"
                        "from .schemas import BookQuery\n"
                        "from .services.recommendation_service import recommend_books\n\n"
                        "router = APIRouter()\n\n"
                        "@router.post('/recommend')\n"
                        "def get_recommendations(query: BookQuery):\n"
                        "    return recommend_books(query)"
                    ),
                    "schemas.py": (
                        "# Pydantic models\n"
                        "from pydantic import BaseModel\n\n"
                        "class BookQuery(BaseModel):\n"
                        "    genre: str\n"
                        "    author: str = None\n"
                        "    min_rating: float = 0.0"
                    ),
                    "services": {
                        "__init__.py": "",
                        "book_service.py": "# Logic related to books",
                        "recommendation_service.py": (
                            "# Recommendation logic\n"
                            "def recommend_books(query):\n"
                            "    # Dummy logic\n"
                            "    return {'recommendations': ['Book A', 'Book B']}"
                        ),
                    },
                    "data": {
                        "__init__.py": "",
                        "data_loader.py": "# Functions for loading book data",
                        "books.csv": (
                            "book_id,title,author,genre,rating\n"
                            "1,1984,George Orwell,Dystopian,4.6\n"
                            "2,Dune,Frank Herbert,Science Fiction,4.5"
                        ),
                    },
                },
                "requirements.txt": "fastapi\nuvicorn\npydantic\npandas",
                "README.md": "# Book Recommender\n\nA FastAPI-based book recommendation system.",
            }
        }
        self.update_tree_view()
        self.status.config(text="Loaded sample book_recommender structure")


def main():
    parser = argparse.ArgumentParser(description='Project structure generator')
    parser.add_argument('--json', help='JSON file containing project structure')
    parser.add_argument('--output', default='.', help='Output directory for generated project')
    parser.add_argument('--gui', action='store_true', help='Launch GUI designer')
    
    args = parser.parse_args()
    
    if args.gui:
        root = Tk()
        app = ProjectDesigner(root)
        root.mainloop()
    elif args.json:
        ProjectGenerator.create_from_json(args.json, args.output)
    else:
        print("Please specify either --gui or --json argument")
        parser.print_help()

if __name__ == "__main__":
    main()