import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/index.css'
import App from './routes/AppRoutes.jsx'
import { AuthProvider } from './context/authContext.jsx'
import { Amplify } from "aws-amplify";
import awsconfig from "./utils/amplify-outputs.js";

Amplify.configure(awsconfig);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </StrictMode>,
)