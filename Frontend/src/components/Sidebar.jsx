import { Link, useLocation } from "react-router-dom";

function Sidebar() {
      const location = useLocation();

      const menuItem = (path, title) => (
            <Link
                  to={path}
                  className={`block px-3 py-2 rounded-lg transition ${location.pathname === path
                              ? "bg-cyan-500 text-white font-semibold"
                              : "text-gray-300 hover:bg-slate-800 hover:text-white"
                        }`}
            >
                  {title}
            </Link>
      );

      return (
            <aside className="w-64 bg-slate-900 border-r border-slate-800 p-5 min-h-screen">
                  <h2 className="text-xl font-bold text-white mb-8">
                        HyperVisorX
                  </h2>

                  <nav className="space-y-2">
                        {menuItem("/dashboard", "Dashboard")}
                        {menuItem("/console", "Console")}
                        {menuItem("/snapshots", "Snapshots")}
                  </nav>
            </aside>
      );
}

export default Sidebar;