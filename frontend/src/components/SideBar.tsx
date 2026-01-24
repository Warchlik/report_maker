import { NavLink } from 'react-router-dom';
import { Upload, FileText, LogIn, UserPlus } from 'lucide-react';
import { cn } from '../lib/utils';

const Sidebar = () => {
  const navItems = [
    { to: "/", icon: Upload, label: "Upload" },
    { to: "/history", icon: FileText, label: "Historia" },
    { to: "/login", icon: LogIn, label: "Logowanie" },
    { to: "/register", icon: UserPlus, label: "Rejestracja" },
  ];

  return (
    <aside
      className="fixed left-0 top-0 z-40 h-screen w-[60px] border-r bg-background transition-[width] duration-300 ease-in-out hover:w-[240px] group shadow-lg"
    >
      <div className="flex h-full flex-col py-4">
        {/* Logo / Brand Area */}
        <div className="flex h-12 items-center justify-center border-b px-2 mb-4 group-hover:justify-start group-hover:px-6 transition-all">
          <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center shrink-0">
            <span className="text-primary-foreground font-bold text-xs">FR</span>
          </div>
          <span className="ml-3 font-bold text-lg opacity-0 transition-opacity duration-300 group-hover:opacity-100 whitespace-nowrap overflow-hidden">
            FileReporter
          </span>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 space-y-2 px-2">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                cn(
                  "flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground",
                  isActive ? "bg-accent text-accent-foreground" : "text-muted-foreground",
                  "justify-center group-hover:justify-start"
                )
              }
            >
              <item.icon className="h-5 w-5 shrink-0" />
              <span className="ml-3 opacity-0 transition-opacity duration-300 group-hover:opacity-100 whitespace-nowrap overflow-hidden">
                {item.label}
              </span>
            </NavLink>
          ))}
        </nav>
      </div>
    </aside>
  );
};

export default Sidebar;
