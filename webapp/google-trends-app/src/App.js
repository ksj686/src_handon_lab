// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div>
        {/* 탭 메뉴 */}
        <div style={{ display: 'flex', cursor: 'pointer' }}>
          <Link to="/tab1" style={{ margin: '0 10px' }}>Tab 1</Link>
          <Link to="/tab2" style={{ margin: '0 10px' }}>Tab 2</Link>
          <Link to="/tab3" style={{ margin: '0 10px' }}>Tab 3</Link>
          <Link to="/tab4" style={{ margin: '0 10px' }}>Tab 4</Link>
          <Link to="/tab5" style={{ margin: '0 10px' }}>Tab 5</Link>
        </div>

        {/* 탭에 해당하는 컴포넌트들 */}
        <Switch>
          <Route path="/tab1" exact>
            <div>Content for Tab 1</div>
          </Route>
          <Route path="/tab2" exact>
            <div>Content for Tab 2</div>
          </Route>
          <Route path="/tab3" exact>
            <div>Content for Tab 3</div>
          </Route>
          <Route path="/tab4" exact>
            <div>Content for Tab 4</div>
          </Route>
          <Route path="/tab5" exact>
            <div>Content for Tab 5</div>
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;