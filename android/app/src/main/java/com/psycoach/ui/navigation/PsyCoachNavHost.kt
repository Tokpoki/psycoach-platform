package com.psycoach.ui.navigation

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import androidx.compose.runtime.remember
import com.psycoach.ui.screen.login.LoginScreen
import com.psycoach.ui.screen.minigame.MiniGameScreen
import com.psycoach.ui.screen.progress.ProgressScreen
import com.psycoach.ui.screen.scenario.ScenarioDetailScreen
import com.psycoach.ui.screen.scenario.ScenarioListScreen
import com.psycoach.viewmodel.AuthViewModel
import com.psycoach.viewmodel.ProgressViewModel
import com.psycoach.viewmodel.ScenarioViewModel

@Composable
fun PsyCoachNavHost(
    navController: NavHostController,
    startDestination: String
) {
    NavHost(navController = navController, startDestination = startDestination) {
        composable(NavRoutes.Login.route) {
            val authViewModel: AuthViewModel = hiltViewModel()
            val authState by authViewModel.authState.collectAsState()
            LoginScreen(
                authState = authState,
                onLogin = { email, password -> authViewModel.login(email, password) },
                onRegister = { email, password, role ->
                    authViewModel.register(email, password, role)
                },
                onNavigateToScenarios = {
                    navController.navigate(NavRoutes.Scenarios.route) {
                        popUpTo(NavRoutes.Login.route) { inclusive = true }
                    }
                }
            )
        }

        composable(NavRoutes.Scenarios.route) {
            val scenarioViewModel: ScenarioViewModel = hiltViewModel()
            val scenarioState by scenarioViewModel.scenarioListState.collectAsState()
            LaunchedEffect(Unit) {
                scenarioViewModel.getScenarios()
            }
            ScenarioListScreen(
                scenarioState = scenarioState,
                onRefresh = { role, kind -> scenarioViewModel.getScenarios(role, kind) },
                onScenarioClick = { id ->
                    navController.navigate(NavRoutes.ScenarioDetail.createRoute(id))
                },
                onOpenProgress = {
                    navController.navigate(NavRoutes.Progress.route)
                }
            )
        }

        composable(
            route = NavRoutes.ScenarioDetail.route,
            arguments = listOf(navArgument("scenarioId") { type = NavType.IntType })
        ) { backStackEntry ->
            val parentEntry = remember(backStackEntry) {
                navController.getBackStackEntry(NavRoutes.Scenarios.route)
            }
            val scenarioViewModel: ScenarioViewModel = hiltViewModel(parentEntry)
            val scenarioState by scenarioViewModel.scenarioDetailState.collectAsState()
            val choiceState by scenarioViewModel.choiceResultState.collectAsState()
            val scenarioId = backStackEntry.arguments?.getInt("scenarioId") ?: return@composable
            LaunchedEffect(scenarioId) {
                scenarioViewModel.getScenarioById(scenarioId)
            }
            ScenarioDetailScreen(
                scenarioState = scenarioState,
                choiceState = choiceState,
                onChoiceSelected = { choiceId ->
                    scenarioViewModel.chooseOption(scenarioId, choiceId)
                },
                onBack = {
                    scenarioViewModel.clearChoiceResult()
                    navController.popBackStack()
                }
            )
        }

        composable(NavRoutes.Progress.route) {
            val progressViewModel: ProgressViewModel = hiltViewModel()
            val progressState by progressViewModel.progressState.collectAsState()
            LaunchedEffect(Unit) {
                progressViewModel.getProgress()
            }
            ProgressScreen(
                progressState = progressState,
                onRefresh = { progressViewModel.getProgress() },
                onPlayMiniGame = { navController.navigate(NavRoutes.MiniGame.route) },
                onBack = { navController.popBackStack() }
            )
        }

        composable(NavRoutes.MiniGame.route) {
            val parentEntry = remember(navController) {
                navController.getBackStackEntry(NavRoutes.Progress.route)
            }
            val progressViewModel: ProgressViewModel = hiltViewModel(parentEntry)
            MiniGameScreen(
                onSubmitScore = { score ->
                    progressViewModel.sendMiniGameResult(type = "focus", score = score)
                    navController.popBackStack()
                },
                onBack = { navController.popBackStack() }
            )
        }
    }
}
