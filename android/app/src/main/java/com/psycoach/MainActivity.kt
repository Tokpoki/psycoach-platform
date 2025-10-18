package com.psycoach

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.compose.rememberNavController
import com.psycoach.ui.navigation.NavRoutes
import com.psycoach.ui.navigation.PsyCoachNavHost
import com.psycoach.ui.theme.PsyCoachTheme
import com.psycoach.viewmodel.AuthViewModel
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            PsyCoachTheme {
                val authViewModel: AuthViewModel = hiltViewModel()
                val tokenState by authViewModel.authToken.collectAsState()
                val startDestination = if (tokenState != null) {
                    NavRoutes.Scenarios.route
                } else {
                    NavRoutes.Login.route
                }
                PsyCoachAppContent(startDestination = startDestination)
            }
        }
    }
}

@Composable
fun PsyCoachAppContent(startDestination: String) {
    val navController = rememberNavController()
    PsyCoachNavHost(navController = navController, startDestination = startDestination)
}
