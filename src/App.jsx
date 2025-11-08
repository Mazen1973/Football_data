import { useState, useEffect } from 'react'
import './App.css'
import Teams from './components/Teams'
import Standings from './components/Standings'
import Fixtures from './components/Fixtures'
import TopScorers from './components/TopScorers'

function App() {
  const [activeTab, setActiveTab] = useState('standings')

  return (
    <div className="app">
      <header className="app-header">
        <h1>⚽ Football Data Dashboard</h1>
        <p>Premier League 2023</p>
      </header>

      <nav className="tabs">
        <button
          className={activeTab === 'standings' ? 'active' : ''}
          onClick={() => setActiveTab('standings')}
        >
          Standings
        </button>
        <button
          className={activeTab === 'teams' ? 'active' : ''}
          onClick={() => setActiveTab('teams')}
        >
          Teams
        </button>
        <button
          className={activeTab === 'fixtures' ? 'active' : ''}
          onClick={() => setActiveTab('fixtures')}
        >
          Fixtures
        </button>
        <button
          className={activeTab === 'scorers' ? 'active' : ''}
          onClick={() => setActiveTab('scorers')}
        >
          Top Scorers
        </button>
      </nav>

      <main className="content">
        {activeTab === 'standings' && <Standings />}
        {activeTab === 'teams' && <Teams />}
        {activeTab === 'fixtures' && <Fixtures />}
        {activeTab === 'scorers' && <TopScorers />}
      </main>
    </div>
  )
}

export default App

