# OCC Doc Assist

A web-based document processing and analysis application built with Streamlit and Azure services. This application allows users to upload documents and receive AI-powered insights and analysis.

## Features

- **Document Upload**: Support for PDF, DOCX, and TXT file formats
- **AI-Powered Analysis**: Automated document processing and insight generation
- **Azure Integration**: Secure cloud storage and processing using Azure services
- **User-Friendly Interface**: Clean, branded web interface with OCC styling
- **Download Results**: Fetch and download processed document insights in Markdown format

## Prerequisites

- Python 3.12 or higher
- Azure Storage Account with:
  - Blob Storage container
  - Queue Storage
- Azure credentials and connection strings

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/eldong/webapp.git
   cd webapp
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file or set the following environment variables:
   ```
   DOCUMENT_STORAGE_CONNECTIONSTRING=your_azure_storage_connection_string
   STORAGE_ACCOUNT_CONTAINER=your_blob_container_name
   TEMPLATE_DOCUMENT_QUEUE=your_queue_name
   STORAGE_ACCOUNT_OUTPUT_CONTAINER=your_output_container_name
   ```

## Running the Application

### Local Development

Run the application locally using the provided script:

```bash
./run.sh
```

Or run directly with Streamlit:

```bash
streamlit run home.py --server.port 8000 --server.address 0.0.0.0
```

The application will be available at `http://localhost:8000`

### Production Deployment

The application is configured for deployment to Azure App Service via GitHub Actions. The deployment pipeline:

1. Builds the Python application
2. Installs dependencies
3. Deploys to Azure App Service (`occaiportalpoc`)

## Usage

1. **Access the Application**: Navigate to the application URL
2. **Upload Documents**: Use the file uploader to select PDF, DOCX, or TXT files
3. **Processing**: The system automatically uploads files to Azure Storage and triggers processing
4. **Fetch Results**: Click the "Fetch" button to retrieve processed insights
5. **Download**: Use the download button to save the generated analysis as a Markdown file

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend Processing**: Azure Functions/Services for document analysis
- **Storage**: Azure Blob Storage for file storage
- **Queue Management**: Azure Queue Storage for processing coordination
- **Authentication**: Microsoft Authentication Library (MSAL)
- **Deployment**: Azure App Service with GitHub Actions CI/CD

## Architecture

```
User → Streamlit App → Azure Blob Storage → Processing Pipeline → Results
                  ↓
              Azure Queue Storage (status tracking)
```

## File Structure

```
webapp/
├── home.py              # Main Streamlit application
├── utils.py             # Utility functions for Azure integration
├── requirements.txt     # Python dependencies
├── run.sh              # Application startup script
├── images/             # UI assets (logos, backgrounds)
├── .github/workflows/  # GitHub Actions deployment pipeline
└── oldpages/           # Legacy/archived components
```

## Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DOCUMENT_STORAGE_CONNECTIONSTRING` | Azure Storage connection string | `DefaultEndpointsProtocol=https;...` |
| `STORAGE_ACCOUNT_CONTAINER` | Input blob container name | `documents` |
| `TEMPLATE_DOCUMENT_QUEUE` | Queue for processing status | `document-queue` |
| `STORAGE_ACCOUNT_OUTPUT_CONTAINER` | Output blob container name | `processed-docs` |

### Azure Services Setup

1. **Create Azure Storage Account**
2. **Create containers**: Input and output blob containers
3. **Create queue**: For processing status tracking
4. **Configure access permissions** for the application

## Security and Compliance

This application is designed for use with sensitive documents. Please ensure:

- Proper Azure security configurations
- Network access controls
- Authentication and authorization setup
- Compliance with organizational data handling policies

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/new-feature`)
7. Create a Pull Request

## Troubleshooting

### Common Issues

- **Connection Errors**: Verify Azure connection strings and network connectivity
- **Upload Failures**: Check Azure Storage permissions and container configuration
- **Processing Delays**: Monitor Azure Queue Storage for processing status

### Logs

Check Streamlit logs and Azure service logs for detailed error information.

## License

This project is intended for internal use within the Office of the Comptroller of the Currency (OCC).

## Support

For technical support or questions, please contact the development team or create an issue in the repository.

---

*Disclaimer: When using Generative Artificial Intelligence (AI) services, you are accountable for ensuring the accuracy and integrity of all AI-generated products that you integrate into your OCC tasks and work products, in alignment with applicable agency-wide or organizational unit standards.*