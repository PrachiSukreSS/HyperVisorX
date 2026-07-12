function Sidebar() {
      return (
            <aside className="w-64 bg-slate-900 border-r border-slate-800 p-5">
                  <ul className="space-y-4 text-gray-300">
                        <li className="text-cyan-400 font-semibold">Dashboard</li>
                        <li>Virtual Machines</li>
                        <li>Snapshots</li>
                        <li>Monitoring</li>
                        <li>Settings</li>
                  </ul>
            </aside>
      );
}

export default Sidebar;