import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [apiData, setApiData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
        setIsLoading(true);
        setIsError(false);
        try {
          const result = await axios.get(
            '/results'
          );
          setIsLoading(false);
          setApiData(result.data);
        }
        catch (error) {
          setIsLoading(false);
          setIsError(true);
        }
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <h1>Results</h1>
      <p>Latest video measurement grouped by video and channel .</p>
      <ul>
        {
          apiData.map(result => (
          <li key={result.id}>
            <h2>{result.video.title}</h2> 
            <p>{result.measurement_date} | <strong>Channel: {result.video.channel.name}</strong></p>
          likes: <span>{result.unsub_likes}</span> |
          dislikes: <span>{result.unsub_dislikes}</span> |
          shares: <span>{result.unsub_shares}</span> |
          views: <span>{result.unsub_views}</span> |
          subscribers gained: <span>{result.subscribersgained}</span> |
          subscribers lost: <span>{result.subscriberslost}</span>
          </li>
          ))
        }
      </ul>
    </div>
  );
}

export default App;
