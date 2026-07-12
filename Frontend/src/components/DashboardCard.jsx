function DashboardCard({ title, value, unit }) {
      return (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg">
                  <h3 className="text-gray-400 text-sm">{title}</h3>

                  <div className="mt-3 text-4xl font-bold text-cyan-400">
                        {value}
                        <span className="text-xl ml-1">{unit}</span>
                  </div>
            </div>
      );
}

export default DashboardCard;