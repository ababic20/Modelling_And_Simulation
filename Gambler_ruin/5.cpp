#include <iostream>
#include <random>
#include <thread>
#include <vector>
#include <chrono>
#include <atomic>
#include <cmath>

double simulateGame(int n, int m, std::atomic<long long>& progressCounter, long long totalExperiments) {
    std::mt19937 rng(std::random_device{}());
    std::uniform_real_distribution<double> dist(0.0, 1.0);

    int currentMoney = n;
    while (currentMoney > 0 && currentMoney < n + m) {
        double outcome = dist(rng);
        if (outcome < 9.0 / 19.0) {
            currentMoney += 1;
        } else {
            currentMoney -= 1;
        }
    }

    ++progressCounter;
    return currentMoney >= n + m ? 1.0 : 0.0;
}

void runSimulations(int n, int m, long long numExperiments, std::atomic<long long>& successfulGames, std::atomic<long long>& progressCounter) {
    long long successes = 0;
    for (long long i = 0; i < numExperiments; i++) {
        successes += simulateGame(n, m, progressCounter, numExperiments);
    }
    successfulGames += successes;
}

double estimateWinningProbability(int n, int m, long long N, int numThreads, std::chrono::steady_clock::time_point startTime) {
    std::atomic<long long> successfulGames(0);
    std::atomic<long long> progressCounter(0);
    std::vector<std::thread> threads;
    long long simulationsPerThread = N / numThreads;

    for (int i = 0; i < numThreads; i++) {
        threads.emplace_back(runSimulations, n, m, simulationsPerThread, std::ref(successfulGames), std::ref(progressCounter));
    }

    long long lastProgress = 0;
    while (progressCounter < N) {
        long long completed = progressCounter;
        auto now = std::chrono::steady_clock::now();
        std::chrono::duration<double> elapsed = now - startTime;
        double elapsedSeconds = elapsed.count();
        
        double remainingTime = (elapsedSeconds / completed) * (N - completed);
        int remainingMinutes = static_cast<int>(remainingTime) / 60;
        int remainingSeconds = static_cast<int>(remainingTime) % 60;

        if (completed > lastProgress) {
            std::cout << "\rProgress: " << (completed * 100) / N << "% Remaining time: "
                      << remainingMinutes << "m " << remainingSeconds << "s " << std::flush;
            lastProgress = completed;
        }
    }

    for (auto& thread : threads) {
        thread.join();
    }

    return static_cast<double>(successfulGames) / N;
}

double calculateAnalyticalProbability(int n, int m, double q) {
    double Z = (1 / q) - 1;
    double Zn = std::pow(Z, n);
    double Znm = std::pow(Z, n + m);

    return (Zn - 1) / (Znm - 1);
}

void performTest(int n, int m, long long N, int numThreads) {
    auto start = std::chrono::steady_clock::now();
    double winProbability = estimateWinningProbability(n, m, N, numThreads, start);
    auto end = std::chrono::steady_clock::now();
    std::chrono::duration<double> duration = end - start;

    std::cout << "\rProgress: 100% Remaining time: 0m 0s\n";
    std::cout << "Winning Probability: " << winProbability << std::endl;

    double q = 9.0 / 19.0;
    double analyticalProbability = calculateAnalyticalProbability(n, m, q);
    std::cout << "Theoretical Winning Probability: " << analyticalProbability << std::endl;

    std::cout << "Time taken for computation: " << duration.count() << " seconds" << std::endl;
}

void displayMenu() {
    std::cout << "\nTesting menu:\n";
    std::cout << "1. Test n=10, m=10, N=1000000\n";
    std::cout << "2. Test n=100, m=100, N=1000000\n";
    std::cout << "3. Test n=20, m=150, N=10000000\n";
    std::cout << "Select test case (1/2/3): ";
}

int main() {
    int numThreads = std::thread::hardware_concurrency(); 
    bool continueTesting = true;

    while (continueTesting) {
        displayMenu();

        int choice;
        std::cin >> choice;

        int n, m;
        long long N;
        switch (choice) {
            case 1:
                n = 10; m = 10; N = 1000000;
                break;
            case 2:
                n = 100; m = 100; N = 1000000;
                break;
            case 3:
                n = 20; m = 150; N = 100000000;
                break;
            default:
                std::cout << "Invalid choice! Please try again.\n";
                continue;
        }

        std::cout << "\nRunning test case n=" << n << ", m=" << m << ", N=" << N << std::endl;
        performTest(n, m, N, numThreads);

        std::string response;
        std::cout << "Do you want to continue with another test? (yes/no): ";
        std::cin >> response;
        if (response != "yes") {
            continueTesting = false;
            std::cout << "Exiting program." << std::endl;
        }
    }

    return 0;
}
