# Setting Up Qdrant Dashboard on Windows

Follow the steps below to set up Qdrant and its Web UI (Dashboard).

## 1. Create the Main Folder

Create the following folder:

```text
C:\AIAgents_Projects
```

## 2. Copy Qdrant Executable

Copy the `qdrant.exe` file into:

```text
C:\AIAgents_Projects
```

## 3. Create Your Project Folder

Your project folder should be created inside `C:\AIAgents_Projects`.

Example:

```text
C:\AIAgents_Projects\event-search-agent
```

## 4. Download Qdrant Web UI

Visit the official Qdrant Web UI releases page:

https://github.com/qdrant/qdrant-web-ui/releases

## 5. Download the Dashboard ZIP File

Download the file named:

```text
dist-qdrant.zip
```

Direct download URL:

https://github.com/qdrant/qdrant-web-ui/releases/download/v0.2.12/dist-qdrant.zip

## 6. Extract the ZIP File

Extract the downloaded ZIP file.

After extraction, the folder structure will look similar to:

```text
dist-qdrant
│
└── dist
    │
    ├── index.html
    ├── assets
    └── ...
```

## 7. Create the Static Folder

Create a folder named:

```text
C:\AIAgents_Projects\static
```

## 8. Copy Dashboard Files

Copy all files and folders from:

```text
Drive:\dist-qdrant\dist
```

into:

```text
C:\AIAgents_Projects\static
```

After copying, the structure should look similar to:

```text
C:\AIAgents_Projects
│
├── qdrant.exe
├── static
│   ├── index.html
│   ├── assets
│   └── ...
```

## 9. Start Qdrant and Open the Dashboard

Run:

```text
qdrant.exe
```

Open a web browser and navigate to:

```text
http://localhost:6333/dashboard
```

If everything is configured correctly, the Qdrant Dashboard will open successfully.