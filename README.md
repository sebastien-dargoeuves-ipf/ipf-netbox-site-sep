# Site Separation with NetBox

This script updates the Global Attributes in IP Fabric based on site information from NetBox. It fetches devices from NetBox, builds a dictionary of attributes, and optionally pushes these attributes to IP Fabric. It also handles devices with serial numbers containing a `/`.

## Requirements

- Python 3.8 or higher
- The following Python packages:
  - `pynetbox`
  - `ipfabric`
  - `loguru`
  - `python-dotenv`

## Installation

1. Clone the repository.

2. Install the required Python packages:

  ```bash
  pip install -r requirements.txt
  ```

3. Create a `.env` file in the root directory of the project and add the necessary environment variables.  The script uses `dotenv` to load environment variables from this file.

## Configuration

### Environment Variables

The script uses the following environment variables, which should be defined in a `.env` file:

- `NETBOX_URL`: The URL of the NetBox instance.
- `NETBOX_TOKEN`: The authentication token for NetBox.
- `IPF_URL`: The URL of the IP Fabric instance.
- `IPF_TOKEN`: The authentication token for IP Fabric.
- `IPF_VERIFY`: Whether to verify the SSL certificate of the IP Fabric instance. This should be a boolean value (`True` or `False`). Default is `False`.

## Usage

You can run the script using the following command:

\```
python site-sep-netbox.py
\```

## Script Details

### Functions

- `initiate_ipf(settings)`: Initializes and returns an IP Fabric client instance.
- `initiate_nb_api(settings)`: Initializes and returns a NetBox API client instance.
- `update_global_attributes(ipf, nbApi, ipf_url)`: Fetches devices from NetBox, builds a dictionary of attributes, and optionally pushes these attributes to IP Fabric.

### Main Execution

The script's main execution function does the following:

1. Initializes the IP Fabric and NetBox API clients.
2. Fetches devices from NetBox and builds a dictionary of attributes based on the serial numbers and site information.
3. Prompts the user to push the new attributes to IP Fabric.
4. Fetches devices from IP Fabric and builds a list of extra attributes for devices with serial numbers containing a `/`.
5. Prompts the user to push the extra attributes to IP Fabric.

### Example Usage

Here is an example of how to run the script:

\```
python site-sep-netbox.py
\```

## License

This project is licensed under the terms of the MIT license.
