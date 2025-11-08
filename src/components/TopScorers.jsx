import { useState, useEffect } from 'react'
import './TopScorers.css'
import API_BASE_URL from '../config'

function TopScorers() {
  const [scorers, setScorers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/top-scorers`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch top scorers')
        return res.json()
      })
      .then(data => {
        setScorers(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) return <div className="loading">Loading top scorers...</div>
  if (error) return <div className="error">Error: {error}</div>

  return (
    <div className="top-scorers">
      <h2>Top Scorers</h2>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Player</th>
              <th>Team</th>
              <th>Position</th>
              <th>Nationality</th>
              <th>Age</th>
              <th>Goals</th>
              <th>Assists</th>
              <th>Apps</th>
              <th>Shots</th>
              <th>On Target</th>
            </tr>
          </thead>
          <tbody>
            {scorers.map((player, index) => (
              <tr key={player.player_id}>
                <td className="rank">{index + 1}</td>
                <td className="player-name">{player.player_name}</td>
                <td>{player.team_name || '-'}</td>
                <td>{player.position || '-'}</td>
                <td>{player.nationality || '-'}</td>
                <td>{player.age || '-'}</td>
                <td className="goals"><strong>{player.goals || 0}</strong></td>
                <td>{player.assists || 0}</td>
                <td>{player.appearances || 0}</td>
                <td>{player.shots_total || 0}</td>
                <td>{player.shots_on_target || 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default TopScorers

