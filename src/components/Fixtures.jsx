import { useState, useEffect } from 'react'
import './Fixtures.css'
import API_BASE_URL from '../config'

function Fixtures() {
  const [fixtures, setFixtures] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [viewMode, setViewMode] = useState('all')

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/fixtures`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch fixtures')
        return res.json()
      })
      .then(data => {
        setFixtures(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  const formatDate = (dateString) => {
    if (!dateString) return 'TBD'
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' })
  }

  const getDateKey = (dateString) => {
    if (!dateString) return 'unknown'
    const date = new Date(dateString)
    return date.toISOString().split('T')[0]
  }

  const isCompleted = (fixture) => {
    return fixture.home_goals !== null && fixture.away_goals !== null
  }

  const isUpcoming = (fixture) => {
    if (isCompleted(fixture)) return false
    if (!fixture.date) return true
    const fixtureDate = new Date(fixture.date)
    return fixtureDate >= new Date()
  }

  const groupByDate = (fixturesList) => {
    const grouped = {}
    fixturesList.forEach(fixture => {
      const dateKey = getDateKey(fixture.date)
      if (!grouped[dateKey]) {
        grouped[dateKey] = []
      }
      grouped[dateKey].push(fixture)
    })
    return grouped
  }

  const filterFixtures = () => {
    if (viewMode === 'upcoming') {
      return fixtures.filter(isUpcoming)
    } else if (viewMode === 'completed') {
      return fixtures.filter(isCompleted)
    }
    return fixtures
  }

  const filteredFixtures = filterFixtures()
  const groupedFixtures = groupByDate(filteredFixtures)
  const sortedDates = Object.keys(groupedFixtures).sort()

  if (loading) return <div className="loading">Loading fixtures...</div>
  if (error) return <div className="error">Error: {error}</div>

  return (
    <div className="fixtures">
      <div className="fixtures-header">
        <h2>Fixtures</h2>
        <div className="view-toggle">
          <button
            className={viewMode === 'all' ? 'active' : ''}
            onClick={() => setViewMode('all')}
          >
            All
          </button>
          <button
            className={viewMode === 'upcoming' ? 'active' : ''}
            onClick={() => setViewMode('upcoming')}
          >
            Upcoming
          </button>
          <button
            className={viewMode === 'completed' ? 'active' : ''}
            onClick={() => setViewMode('completed')}
          >
            Completed
          </button>
        </div>
      </div>

      {filteredFixtures.length === 0 ? (
        <div className="no-data">No fixtures available</div>
      ) : (
        <div className="fixtures-list">
          {sortedDates.map((dateKey) => {
            const dateFixtures = groupedFixtures[dateKey]
            const firstFixture = dateFixtures[0]
            const displayDate = formatDate(firstFixture.date)
            
            return (
              <div key={dateKey} className="date-group">
                <div className="date-header">
                  <h3>{displayDate}</h3>
                  {firstFixture.round && (
                    <span className="round-badge">{firstFixture.round}</span>
                  )}
                </div>
                <div className="date-fixtures">
                  {dateFixtures.map((fixture) => (
                    <div key={fixture.fixture_id} className="fixture-card">
                      <div className="fixture-teams">
                        <div className="team home-team">
                          <div className="team-name">{fixture.home_team_name}</div>
                        </div>
                        {fixture.home_goals !== null && fixture.away_goals !== null ? (
                          <div className="score-container">
                            <span className="score home-score">{fixture.home_goals}</span>
                            <span className="score-separator">-</span>
                            <span className="score away-score">{fixture.away_goals}</span>
                          </div>
                        ) : (
                          <div className="vs">vs</div>
                        )}
                        <div className="team away-team">
                          <div className="team-name">{fixture.away_team_name}</div>
                        </div>
                      </div>
                      <div className="fixture-footer">
                        <div className="fixture-info">
                          {fixture.time && (
                            <span className="time">🕐 {fixture.time}</span>
                          )}
                          {fixture.venue_name && (
                            <span className="venue">📍 {fixture.venue_name}{fixture.venue_city && `, ${fixture.venue_city}`}</span>
                          )}
                        </div>
                        {fixture.status && (
                          <div className={`status ${fixture.status.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')}`}>
                            {fixture.status}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default Fixtures

