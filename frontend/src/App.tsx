import { HashRouter, Outlet, Route, Routes } from "react-router-dom";
import Sidebar from "./components/SideBar";
import UploadPage from "./pages/UploadPage";
import HistoryPage from "./pages/HisoryPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";

const Layout = () => {
  return (
    <div className="flex min-h-screen w-full bg-background text-foreground">
      <Sidebar />
      <main className="ml-[60px] min-h-screen w-full transition-all duration-300">
        <Outlet />
      </main>
    </div>
  );
};

// TODO: do poprawy wygląd oraz informacje, podpiąć endpointy po zrobieniu backendu
export default function App() {
  return (
    <>
      <HashRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<UploadPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
          </Route>
        </Routes>
      </HashRouter>
    </>
  );
}

