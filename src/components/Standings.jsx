import { useState, useEffect } from 'react'
import './Standings.css'
import API_BASE_URL from '../config'

function Standings() {
  const [standings, setStandings] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/standings`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch standings')
        return res.json()
      })
      .then(data => {
        setStandings(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) return <div className="loading">Loading standings...</div>
  if (error) return <div className="error">Error: {error}</div>

  return (
    <div className="standings">
      <h2>Premier League Standings</h2>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Pos</th>
              <th>Team</th>
              <th>P</th>
              <th>W</th>
              <th>D</th>
              <th>L</th>
              <th>GF</th>
              <th>GA</th>
              <th>GD</th>
              <th>Pts</th>
              <th>Form</th>
            </tr>
          </thead>
          <tbody>
            {standings.map((team) => (
              <tr key={team.team_id}>
                <td className="position">{team.position}</td>
                <td className="team-name">{team.team_name}</td>
                <td>{team.played || 0}</td>
                <td>{team.wins || 0}</td>
                <td>{team.draws || 0}</td>
                <td>{team.loses || 0}</td>
                <td>{team.goals_for || 0}</td>
                <td>{team.goals_against || 0}</td>
                <td className={team.goals_diff >= 0 ? 'positive' : 'negative'}>
                  {team.goals_diff >= 0 ? '+' : ''}{team.goals_diff || 0}
                </td>
                <td className="points"><strong>{team.points || 0}</strong></td>
                <td className="form">{team.form || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Standings

