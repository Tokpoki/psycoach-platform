package com.psycoach.ui.navigation

sealed class NavRoutes(val route: String) {
    object Login : NavRoutes("login")
    object Scenarios : NavRoutes("scenarios")
    object ScenarioDetail : NavRoutes("scenario/{scenarioId}") {
        fun createRoute(id: Int) = "scenario/$id"
    }
    object Progress : NavRoutes("progress")
    object MiniGame : NavRoutes("minigame")
}
