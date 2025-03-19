## Installation

1. Clone this repository
2. Create a virtual environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
python3 src/main.py input_path.ifc output_path.glb [export_type]
```

Parameters:

- `input_path.ifc`: Path to the input IFC file
- `output_path.glb`: Path for the output GLB or glTF file (.glb or .gltf extension)
- `export_type` (optional): Type of export
  - `properties` (default): Include property data in the export
  - `model_only`: Export only geometry without property data

### Examples

Export with properties (default):

```bash
python3 src/main.py building.ifc building.glb
```

Export geometry only:

```bash
python main.py building.ifc building.glb model_only
```

Export to glTF format:

```bash
python main.py building.ifc building.gltf
```
