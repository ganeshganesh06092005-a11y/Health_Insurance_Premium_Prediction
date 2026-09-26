// HealthSecure Smart Analytics & Dashboard Filter Controller
(function() {
    'use strict';

    if (typeof window.analyticsData === 'undefined') {
        return;
    }

    const rawRecords = window.analyticsData.records_data || [];
    let charts = {};

    function getFilteredData() {
        const planFilter = document.getElementById('filterPlan')?.value || 'all';
        const smokerFilter = document.getElementById('filterSmoker')?.value || 'all';
        const genderFilter = document.getElementById('filterGender')?.value || 'all';
        const regionFilter = document.getElementById('filterRegion')?.value || 'all';

        return rawRecords.filter(item => {
            if (planFilter !== 'all' && item.plan.toLowerCase() !== planFilter.toLowerCase()) return false;
            if (smokerFilter !== 'all' && item.smoker.toLowerCase() !== smokerFilter.toLowerCase()) return false;
            if (genderFilter !== 'all' && item.sex.toLowerCase() !== genderFilter.toLowerCase()) return false;
            if (regionFilter !== 'all' && item.region.toLowerCase() !== regionFilter.toLowerCase()) return false;
            return true;
        });
    }

    function calculateMetrics(records) {
        const count = records.length;
        if (count === 0) {
            return {
                count: 0,
                avgPremium: 0,
                mostPlan: '—',
                distribution: [],
                agePoints: [],
                bmiPoints: [],
                smokingAvg: [],
                planCounts: [],
                monthlyCounts: []
            };
        }

        const premiums = records.map(r => r.premium);
        const avg = premiums.reduce((a, b) => a + b, 0) / count;

        // Plan counts
        const planCountsMap = {};
        records.forEach(r => {
            const p = r.plan.charAt(0).toUpperCase() + r.plan.slice(1);
            planCountsMap[p] = (planCountsMap[p] || 0) + 1;
        });
        const mostPlan = Object.entries(planCountsMap).sort((a, b) => b[1] - a[1])[0][0];

        // Premium distribution (5 bins)
        const minP = Math.min(...premiums);
        const maxP = Math.max(...premiums);
        const width = Math.max((maxP - minP) / 5, 1);
        const distribution = [];
        for (let i = 0; i < 5; i++) {
            const lower = minP + i * width;
            const upper = i === 4 ? maxP : lower + width;
            const cnt = records.filter(r => (i === 4 ? r.premium >= lower && r.premium <= upper : r.premium >= lower && r.premium < upper)).length;
            distribution.push({
                label: `₹${Math.round(lower).toLocaleString()} - ₹${Math.round(upper).toLocaleString()}`,
                count: cnt
            });
        }

        // Smoker average
        const smokerPrems = records.filter(r => r.smoker.toLowerCase() === 'yes').map(r => r.premium);
        const nonSmokerPrems = records.filter(r => r.smoker.toLowerCase() === 'no').map(r => r.premium);
        const smokingAvg = [
            { label: 'Non-Smoker', premium: nonSmokerPrems.length ? Math.round(nonSmokerPrems.reduce((a,b)=>a+b,0) / nonSmokerPrems.length) : 0 },
            { label: 'Smoker', premium: smokerPrems.length ? Math.round(smokerPrems.reduce((a,b)=>a+b,0) / smokerPrems.length) : 0 }
        ];

        // Monthly counts
        const monthMap = {};
        records.forEach(r => {
            monthMap[r.month] = (monthMap[r.month] || 0) + 1;
        });
        const monthlyCounts = Object.keys(monthMap).sort().map(m => ({ label: m, count: monthMap[m] }));

        return {
            count,
            avgPremium: Math.round(avg),
            mostPlan,
            distribution,
            agePoints: records.map(r => ({ x: r.age, y: r.premium })),
            bmiPoints: records.map(r => ({ x: r.bmi, y: r.premium })),
            smokingAvg,
            planCounts: Object.entries(planCountsMap).map(([label, count]) => ({ label, count })),
            monthlyCounts
        };
    }

    function initCharts() {
        const metrics = calculateMetrics(rawRecords);
        const colors = ['#1677c8', '#0d9b88', '#e5a63b', '#7c6bb1', '#d46a6a'];

        // Chart 1: Premium Distribution
        const ctxDist = document.getElementById('chartPremiumDist')?.getContext('2d');
        if (ctxDist) {
            charts.dist = new Chart(ctxDist, {
                type: 'bar',
                data: {
                    labels: metrics.distribution.map(d => d.label),
                    datasets: [{
                        label: 'Predictions',
                        data: metrics.distribution.map(d => d.count),
                        backgroundColor: '#1677c8',
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
                }
            });
        }

        // Chart 2: Age vs Predicted Premium
        const ctxAge = document.getElementById('chartAgePremium')?.getContext('2d');
        if (ctxAge) {
            charts.age = new Chart(ctxAge, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'Applicant Estimate',
                        data: metrics.agePoints,
                        backgroundColor: '#0d9b88',
                        pointRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: { title: { display: true, text: 'Age (Years)' } },
                        y: { title: { display: true, text: 'Predicted Premium (INR)' } }
                    }
                }
            });
        }

        // Chart 3: BMI vs Predicted Premium
        const ctxBmi = document.getElementById('chartBmiPremium')?.getContext('2d');
        if (ctxBmi) {
            charts.bmi = new Chart(ctxBmi, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'Applicant Estimate',
                        data: metrics.bmiPoints,
                        backgroundColor: '#1677c8',
                        pointRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: { title: { display: true, text: 'Body Mass Index (BMI)' } },
                        y: { title: { display: true, text: 'Predicted Premium (INR)' } }
                    }
                }
            });
        }

        // Chart 4: Smoking Status vs Premium
        const ctxSmoker = document.getElementById('chartSmokerPremium')?.getContext('2d');
        if (ctxSmoker) {
            charts.smoker = new Chart(ctxSmoker, {
                type: 'bar',
                data: {
                    labels: metrics.smokingAvg.map(s => s.label),
                    datasets: [{
                        label: 'Average Annual Premium (INR)',
                        data: metrics.smokingAvg.map(s => s.premium),
                        backgroundColor: ['#0d9b88', '#d46a6a'],
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true } }
                }
            });
        }

        // Chart 5: Plan Recommendation Distribution
        const ctxPlan = document.getElementById('chartPlanDist')?.getContext('2d');
        if (ctxPlan) {
            charts.plan = new Chart(ctxPlan, {
                type: 'doughnut',
                data: {
                    labels: metrics.planCounts.map(p => p.label),
                    datasets: [{
                        data: metrics.planCounts.map(p => p.count),
                        backgroundColor: ['#1677c8', '#0d9b88', '#e5a63b']
                    }]
                },
                options: { responsive: true }
            });
        }

        // Chart 6: Predictions by Month
        const ctxMonth = document.getElementById('chartMonthTrend')?.getContext('2d');
        if (ctxMonth) {
            charts.month = new Chart(ctxMonth, {
                type: 'line',
                data: {
                    labels: metrics.monthlyCounts.map(m => m.label),
                    datasets: [{
                        label: 'Prediction Volume',
                        data: metrics.monthlyCounts.map(m => m.count),
                        borderColor: '#0d9b88',
                        backgroundColor: 'rgba(13, 155, 136, 0.12)',
                        fill: true,
                        tension: 0.3,
                        pointRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
                }
            });
        }
    }

    function updateCharts() {
        const filtered = getFilteredData();
        const metrics = calculateMetrics(filtered);

        // Update KPI values in DOM
        const kpiCount = document.getElementById('kpiTotalPredictions');
        if (kpiCount) kpiCount.textContent = metrics.count;

        const kpiAvg = document.getElementById('kpiAveragePremium');
        if (kpiAvg) kpiAvg.textContent = metrics.count ? `INR ${metrics.avgPremium.toLocaleString()}` : '—';

        const kpiPlan = document.getElementById('kpiMostPlan');
        if (kpiPlan) kpiPlan.textContent = metrics.mostPlan;

        // Update chart datasets
        if (charts.dist) {
            charts.dist.data.labels = metrics.distribution.map(d => d.label);
            charts.dist.data.datasets[0].data = metrics.distribution.map(d => d.count);
            charts.dist.update();
        }
        if (charts.age) {
            charts.age.data.datasets[0].data = metrics.agePoints;
            charts.age.update();
        }
        if (charts.bmi) {
            charts.bmi.data.datasets[0].data = metrics.bmiPoints;
            charts.bmi.update();
        }
        if (charts.smoker) {
            charts.smoker.data.labels = metrics.smokingAvg.map(s => s.label);
            charts.smoker.data.datasets[0].data = metrics.smokingAvg.map(s => s.premium);
            charts.smoker.update();
        }
        if (charts.plan) {
            charts.plan.data.labels = metrics.planCounts.map(p => p.label);
            charts.plan.data.datasets[0].data = metrics.planCounts.map(p => p.count);
            charts.plan.update();
        }
        if (charts.month) {
            charts.month.data.labels = metrics.monthlyCounts.map(m => m.label);
            charts.month.data.datasets[0].data = metrics.monthlyCounts.map(m => m.count);
            charts.month.update();
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        initCharts();

        ['filterPlan', 'filterSmoker', 'filterGender', 'filterRegion'].forEach(id => {
            document.getElementById(id)?.addEventListener('change', updateCharts);
        });

        document.getElementById('btnResetFilters')?.addEventListener('click', () => {
            ['filterPlan', 'filterSmoker', 'filterGender', 'filterRegion'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.value = 'all';
            });
            updateCharts();
        });
    });
})();
