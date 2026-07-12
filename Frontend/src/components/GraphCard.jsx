import {
      Chart as ChartJS,
      CategoryScale,
      LinearScale,
      PointElement,
      LineElement,
      Title,
      Tooltip,
      Legend,
} from "chart.js";

import { Line } from "react-chartjs-2";

ChartJS.register(
      CategoryScale,
      LinearScale,
      PointElement,
      LineElement,
      Title,
      Tooltip,
      Legend
);

function GraphCard({ title, data }) {
      const chartData = {
            labels: data.map((_, index) => index + 1),

            datasets: [
                  {
                        label: title,
                        data: data,
                  },
            ],
      };

      return (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                  <h2 className="mb-4 text-xl font-semibold">
                        {title}
                  </h2>

                  <Line data={chartData} />
            </div>
      );
}

export default GraphCard;