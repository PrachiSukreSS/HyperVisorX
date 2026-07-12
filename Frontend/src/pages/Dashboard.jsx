import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import DashboardCard from "../components/DashboardCard";
import GraphCard from "../components/GraphCard";
import api from "../services/api";

function Dashboard() {
      const [metrics, setMetrics] = useState({
            cpu_usage: 0,
            memory_usage: 0,
            disk_usage: 0,
            network_sent: 0,
            host_usage: 0,
            vm_usage: 0,
      });

      const [cpuHistory, setCpuHistory] = useState([]);
      const [ramHistory, setRamHistory] = useState([]);
      const [diskHistory, setDiskHistory] = useState([]);
      const [networkHistory, setNetworkHistory] = useState([]);

      useEffect(() => {
            fetchMetrics();

            const interval = setInterval(fetchMetrics, 3000);

            return () => clearInterval(interval);
      }, []);

      async function fetchMetrics() {
            try {
                  const res = await api.get("/monitoring");

                  setMetrics(res.data);

                  setCpuHistory((prev) => [
                        ...prev.slice(-19),
                        res.data.cpu_usage,
                  ]);

                  setRamHistory((prev) => [
                        ...prev.slice(-19),
                        res.data.memory_usage,
                  ]);

                  setDiskHistory((prev) => [
                        ...prev.slice(-19),
                        res.data.disk_usage,
                  ]);

                  setNetworkHistory((prev) => [
                        ...prev.slice(-19),
                        res.data.network_sent,
                  ]);

            } catch (err) {
                  console.error(err);
            }
      }

      return (
            <div className="min-h-screen bg-slate-950 text-white">
                  <Navbar />

                  <div className="flex">
                        <Sidebar />

                        <main className="flex-1 p-8">

                              <h2 className="text-3xl font-bold">
                                    Monitoring Dashboard
                              </h2>

                              <p className="text-gray-400 mt-2">
                                    Live Hypervisor Resource Monitoring
                              </p>

                              {/* Monitoring Cards */}
                              <div className="grid grid-cols-3 gap-6 mt-8">

                                    <DashboardCard
                                          title="CPU Usage"
                                          value={metrics.cpu_usage}
                                          unit="%"
                                    />

                                    <DashboardCard
                                          title="RAM Usage"
                                          value={metrics.memory_usage}
                                          unit="%"
                                    />

                                    <DashboardCard
                                          title="Disk Usage"
                                          value={metrics.disk_usage}
                                          unit="%"
                                    />

                                    <DashboardCard
                                          title="Network"
                                          value={metrics.network_sent}
                                          unit="KB"
                                    />

                                    <DashboardCard
                                          title="Host Usage"
                                          value={metrics.host_usage}
                                          unit="%"
                                    />

                                    <DashboardCard
                                          title="VM Usage"
                                          value={metrics.vm_usage}
                                          unit="%"
                                    />

                              </div>

                              {/* Live Graphs */}
                              <div className="grid grid-cols-2 gap-6 mt-10">

                                    <GraphCard
                                          title="CPU Usage"
                                          data={cpuHistory}
                                    />

                                    <GraphCard
                                          title="RAM Usage"
                                          data={ramHistory}
                                    />

                                    <GraphCard
                                          title="Disk Usage"
                                          data={diskHistory}
                                    />

                                    <GraphCard
                                          title="Network Usage"
                                          data={networkHistory}
                                    />

                              </div>

                        </main>
                  </div>
            </div>
      );
}

export default Dashboard;