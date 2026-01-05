import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

import "@refinitiv-ui/elements/button";
import "@refinitiv-ui/elements/panel";
import "@refinitiv-ui/elements/text-field";
import "@refinitiv-ui/elements/email-field";
import "@refinitiv-ui/elements/slider";
import "@refinitiv-ui/elements/radio-button";
import "@refinitiv-ui/elements/datetime-picker";
import "@refinitiv-ui/elements/swing-gauge";
import "@refinitiv-ui/elements/led-gauge";
import "@refinitiv-ui/elements/combo-box";
import "@refinitiv-ui/elements/toggle";
import "@refinitiv-ui/elements/dialog";
import "@refinitiv-ui/elements/pagination";
import "@refinitiv-ui/elements/tab-bar";
import "@refinitiv-ui/elements/tab";

import "@refinitiv-ui/halo-theme/dark/imports/native-elements";
import "@refinitiv-ui/elements/button/themes/halo/dark";
import "@refinitiv-ui/elements/panel/themes/halo/dark";
import "@refinitiv-ui/elements/text-field/themes/halo/dark";
import "@refinitiv-ui/elements/datetime-picker/themes/halo/dark";
import "@refinitiv-ui/elements/swing-gauge/themes/halo/dark";
import "@refinitiv-ui/elements/led-gauge/themes/halo/dark";
import "@refinitiv-ui/elements/radio-button/themes/halo/dark";
import "@refinitiv-ui/elements/combo-box/themes/halo/dark";
import "@refinitiv-ui/elements/toggle/themes/halo/dark";
import "@refinitiv-ui/elements/dialog/themes/halo/dark";
import "@refinitiv-ui/elements/pagination/themes/halo/dark";
import "@refinitiv-ui/elements/tab-bar/themes/halo/dark";
import "@refinitiv-ui/elements/tab/themes/halo/dark";

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
