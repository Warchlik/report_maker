import { SidebarProvider, SidebarTrigger } from "./components/ui/sidebar";
import { BrowserRouter, Outlet, Route, Routes } from "react-router-dom";
import { AppSidebar } from "./components/AppSideBar";
import Upload from "./pages/Upload";


const Layout = () => {
  return (
    <>
      <SidebarProvider>
        <AppSidebar />
        <main className="w-full">
          <SidebarTrigger className="ml-2 mt-2" />
          <Outlet />
        </main>
      </SidebarProvider>
    </>
  )
}


const PlaceHolder = () => {
  return (
    <>

    </>
  )
}

export default function App() {
  // return <ComponentExample />;

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<PlaceHolder />} />
            <Route path="/upload" element={<Upload />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  )
}




// The `tooltip` component has been added. Remember to wrap your app with the `TooltipProvider` component.
//
// ```tsx title="app/layout.tsx"
// import { TooltipProvider } from "@/components/ui/tooltip"
//
// export default function RootLayout({ children }: { children: React.ReactNode }) {
//   return (
//     <html lang="en">
//       <body>
//         <TooltipProvider>{children}</TooltipProvider>
//       </body>
//     </html>
//   )
// }
// ```
