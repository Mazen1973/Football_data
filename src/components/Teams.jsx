import { useState, useEffect } from 'react'
import './Teams.css'
import API_BASE_URL from '../config'

function Teams() {
  const [teams, setTeams] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/teams`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch teams')
        return res.json()
      })
      .then(data => {
        setTeams(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) return <div className="loading">Loading teams...</div>
  if (error) return <div className="error">Error: {error}</div>

  return (
    <div className="teams">
      <h2>Premier League Teams</h2>
      <div className="teams-grid">
        {teams.map((team) => (
          <div key={team.team_id} className="team-card">
            <div className="team-name">{team.name}</div>
            <div className="team-details">
              {team.country && <div className="detail-item">📍 {team.country}</div>}
              {team.founded && <div className="detail-item">Founded: {team.founded}</div>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Teams

