import './App.css'
import { Route, Routes } from 'react-router-dom'
import { DashboardLayout, LoginLayout } from './layout'
import { Home } from './pages'
import { Login } from './pages'
import { List } from './pages'
import { NotFound } from './pages'
import { Discover } from './pages'
import ProtectedRoute from "./components/ProtectedRoute"
import React, { useEffect, useState } from "react";
function App() {
  const [user, setUser] = useState(null)
  return (
    <>
      <Routes>
        <Route path="/login" element={<LoginLayout><Login /></LoginLayout>} />
        <Route
          path="/dashboard/*"
          element={
            <ProtectedRoute isAllowed={!!user}>
              <DashboardLayout>
                <Routes>
                  <Route index element={<Home />} />
                  <Route path="test" element={<List />} />
                  <Route path="api" element={<Discover />} />
                </Routes>
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
        <Route path='*' element={<NotFound />} />
      </Routes>
    </>
  )
}

export default App
