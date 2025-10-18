package com.psycoach.ui.screen.minigame

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun MiniGameScreen(
    onSubmitScore: (Int) -> Unit,
    onBack: () -> Unit
) {
    val scoreState = remember { mutableIntStateOf(0) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(text = "Мини-игра: Реакция", style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(16.dp))
        Text(text = "Очки: ${scoreState.intValue}")
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = { scoreState.intValue += 1 }, modifier = Modifier.fillMaxWidth()) {
            Text(text = "Попасть в ритм")
        }
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = { onSubmitScore(scoreState.intValue) }, modifier = Modifier.fillMaxWidth()) {
            Text(text = "Отправить результат")
        }
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = onBack, modifier = Modifier.fillMaxWidth()) {
            Text(text = "Назад")
        }
    }
}
