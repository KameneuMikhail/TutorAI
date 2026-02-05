# TutorAI Minimal Frontend

This is a minimal Angular app that displays only a title `Tutor AI`.

To run locally:

```bash
cd frontend
npm install --legacy-peer-deps
npx ng serve --open
```

The project uses Angular 21 packages (latest stable at time of creation).

Deployment to Azure Static Web Apps
-----------------------------------

1. Create a Static Web App in the Azure Portal or via the Azure CLI. During creation select the GitHub repo and branch (e.g., `main`) or choose "None" and use the workflow below.

2. Add the deployment token as a GitHub repository secret named `AZURE_STATIC_WEB_APPS_API_TOKEN`. (If you created the Static Web App via the portal you can find the deployment token under "Manage deployment token".)

3. This repository contains a GitHub Actions workflow at `.github/workflows/azure-static-web-apps.yml` which will build the frontend and deploy the contents of `frontend/dist/tutorai-frontend` and connect the Azure Functions API under `backend/azure-functions`.

4. Push to `main` (or the branch configured in the workflow) to trigger the deployment.

Notes:
- The workflow uses `npm ci --legacy-peer-deps` for dependency installation; adjust if you prefer `npm install`.
- Ensure `local.settings.json` values (secrets/config) are set in Azure for the Functions app if your frontend relies on them.
