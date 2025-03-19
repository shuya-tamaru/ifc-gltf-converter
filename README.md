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
python3 src/main.py building.ifc building.glb model_only
```

Export to glTF format:

```bash
python3 src/main.py building.ifc building.gltf
```

### Draco Compression

If you need to apply Draco compression to reduce file size:

Export your model to glTF format:

```bash
python3 src/main.py building.ifc building.gltf
```

Use the separate gltf-pipeline tool for Draco compression. A reference implementation is available at:
https://github.com/shuya-tamaru/gltf-draco-compression

The linked repository provides code examples for applying Draco compression to your exported glTF files, which can significantly reduce file sizes while maintaining visual quality.
