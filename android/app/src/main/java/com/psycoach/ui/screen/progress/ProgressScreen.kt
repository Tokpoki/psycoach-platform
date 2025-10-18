package com.psycoach.ui.screen.progress

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.psycoach.data.model.ProgressResponse
import com.psycoach.domain.util.Result

@Composable
fun ProgressScreen(
    progressState: Result<ProgressResponse>?,
    onRefresh: () -> Unit,
    onPlayMiniGame: () -> Unit,
    onBack: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(text = "Ваш прогресс", style = MaterialTheme.typography.headlineSmall)
        Spacer(modifier = Modifier.height(12.dp))
        Button(onClick = onRefresh, modifier = Modifier.fillMaxWidth()) {
            Text(text = "Обновить")
        }
        Spacer(modifier = Modifier.height(12.dp))
        Button(onClick = onPlayMiniGame, modifier = Modifier.fillMaxWidth()) {
            Text(text = "Играть мини-игру")
        }
        Spacer(modifier = Modifier.height(24.dp))
        when (progressState) {
            is Result.Loading -> Loader()
            is Result.Success -> ProgressCard(progressState.data)
            is Result.Error -> Text(text = progressState.message, color = MaterialTheme.colorScheme.error)
            null -> Text(text = "Нажмите обновить, чтобы получить данные")
        }
        Spacer(modifier = Modifier.weight(1f, true))
        Button(onClick = onBack, modifier = Modifier.fillMaxWidth()) {
            Text(text = "Назад")
        }
    }
}

@Composable
private fun ProgressCard(progress: ProgressResponse) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = "Очки: ${progress.score}", style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.height(8.dp))
            Text(text = "Уровень: ${progress.level}")
            Spacer(modifier = Modifier.height(8.dp))
            Text(text = "Бейджи: ${progress.badges.joinToString(", ")}")
        }
    }
}

@Composable
private fun Loader() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        CircularProgressIndicator()
    }
}
