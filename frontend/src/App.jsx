import { useEffect, useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('');
  const [state_filter, setStatefilter] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  async function handleSearch() {
    setLoading(true);
      await fetch(`http://localhost:8000/search?q=${query}&category=${category}&state=${state_filter}`)
        .then((response) => {
          if (!response.ok) throw new Error('Network error with handling search');
          return response.json();
        })
        .then((data) => setResults(data.results))
        .then(() => setLoading(false))
  };
  return (
    <div>
      <input
        type="text" value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder='Type here'
      />
      <button onClick={handleSearch} >Type Something</button>
      {loading ? <h1>Loading</h1> : results.map(result =>
        <div key={result.source_url}>
          <ul>
            <li>{result.program_name}</li>
            <li>{result.category}</li>
          </ul> 
        </div>
        )
      }
    </div>
  )


/*
"results":[{"program_name":"Alaskan Veteran Benefits Eligibility","category":"HEALTHCARE","jurisdiction":"STATE","state":"Alaska",
"raw_text":"Eligibility for most federal and state benefits is based upon discharge from military service under other than 
dishonorable conditions. Most benefits require active service.  
This means that the service member was in an active-duty status as a member of the Army, Navy, Air Force, Marine Corps, 
Coast Guard, Space Force, National Guard, Reserves, or as a commissioned officer of the Public Health Service, 
Environmental Science Services Administration or National Oceanic and Atmospheric Administration, or its predecessor, 
the Coast and Geodetic Survey.\nPotential Disqualifiers\nDishonorable and bad conduct discharges issued by general 
courts-martial may bar VA benefits.\nVeterans in prison must contact VA to determine eligibility.\nVA benefits will not 
be provided to any Veteran or dependent wanted for an outstanding felony warrant.\nVA Benefits Requiring Wartime 
Service\nSome VA benefits require proof of war time service. 
Under the law, the VA recognizes these periods of war:\nMexican Border Period: May 9, 1916, 
through April 5, 1917, for Veterans who served in Mexico, on its borders or in adjacent waters.\nWorld 
War I: April 6, 1917, through Nov. 11, 1918; for Veterans who served in Russia, April 6, 1917, through April 1, 
1920; extended through July 1, 1921, for Veterans who had at least one day of service between April 6, 1917, and 
Nov. 11, 1918.\nWorld War II: Dec. 7, 1941, through Dec. 31, 1946.\nKorean War: June 27, 1950, through Jan. 31, 1955.
\nVietnam War: Aug. 5, 1964 (Feb. 28, 1961, for Veterans who served \"in country\" before Aug. 5, 1964), through May 
7, 1975.\nGulf War: Aug. 2, 1990, through a date to be set.","source_url":"https://veterans.alaska.gov/benefits",
"score":0.11606434}],"count":1}%*/                         
}
export default App
