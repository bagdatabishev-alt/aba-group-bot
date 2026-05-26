import logging
from datetime import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8715610432:AAF0ZQRWgL0YiMhcIxdwrlNlygOkP0cbD3M"
CHAT_ID = -5250749325

WORDS = [
    # A1 - Beginner
    {"word": "Hello", "transcription": "[həˈloʊ]", "translation": "Сәлем", "example": "Hello! How are you?"},
    {"word": "Water", "transcription": "[ˈwɔːtər]", "translation": "Су", "example": "I drink water every day."},
    {"word": "Food", "transcription": "[fuːd]", "translation": "Тамақ", "example": "This food is delicious."},
    {"word": "House", "transcription": "[haʊs]", "translation": "Үй", "example": "I live in a big house."},
    {"word": "Family", "transcription": "[ˈfæməli]", "translation": "Отбасы", "example": "My family is very kind."},
    {"word": "School", "transcription": "[skuːl]", "translation": "Мектеп", "example": "I go to school every day."},
    {"word": "Book", "transcription": "[bʊk]", "translation": "Кітап", "example": "I read a book at night."},
    {"word": "Dog", "transcription": "[dɒɡ]", "translation": "Ит", "example": "My dog is very friendly."},
    {"word": "Cat", "transcription": "[kæt]", "translation": "Мысық", "example": "The cat is sleeping."},
    {"word": "Car", "transcription": "[kɑːr]", "translation": "Көлік", "example": "My car is red."},
    {"word": "Friend", "transcription": "[frend]", "translation": "Дос", "example": "She is my best friend."},
    {"word": "Happy", "transcription": "[ˈhæpi]", "translation": "Бақытты", "example": "I am very happy today."},
    {"word": "Good", "transcription": "[ɡʊd]", "translation": "Жақсы", "example": "This is a good idea."},
    {"word": "Work", "transcription": "[wɜːrk]", "translation": "Жұмыс", "example": "I work every day."},
    {"word": "Day", "transcription": "[deɪ]", "translation": "Күн", "example": "Today is a beautiful day."},
    {"word": "Night", "transcription": "[naɪt]", "translation": "Түн", "example": "Good night, everyone."},
    {"word": "Sun", "transcription": "[sʌn]", "translation": "Күн (жарық)", "example": "The sun is bright today."},
    {"word": "Time", "transcription": "[taɪm]", "translation": "Уақыт", "example": "What time is it?"},
    {"word": "Love", "transcription": "[lʌv]", "translation": "Махаббат", "example": "I love my family."},
    {"word": "Name", "transcription": "[neɪm]", "translation": "Аты", "example": "My name is Bagdat."},
    {"word": "City", "transcription": "[ˈsɪti]", "translation": "Қала", "example": "I live in a big city."},
    {"word": "Money", "transcription": "[ˈmʌni]", "translation": "Ақша", "example": "I need money to buy food."},
    {"word": "Phone", "transcription": "[foʊn]", "translation": "Телефон", "example": "My phone is new."},
    {"word": "Door", "transcription": "[dɔːr]", "translation": "Есік", "example": "Please close the door."},
    {"word": "Table", "transcription": "[ˈteɪbəl]", "translation": "Үстел", "example": "Put the book on the table."},
    {"word": "Chair", "transcription": "[tʃer]", "translation": "Орындық", "example": "Sit on the chair."},
    {"word": "Window", "transcription": "[ˈwɪndoʊ]", "translation": "Терезе", "example": "Open the window please."},
    {"word": "Bread", "transcription": "[bred]", "translation": "Нан", "example": "I eat bread for breakfast."},
    {"word": "Milk", "transcription": "[mɪlk]", "translation": "Сүт", "example": "Children drink milk."},
    {"word": "Tea", "transcription": "[tiː]", "translation": "Шай", "example": "I drink tea in the morning."},
    {"word": "Apple", "transcription": "[ˈæpəl]", "translation": "Алма", "example": "An apple a day keeps the doctor away."},
    {"word": "Run", "transcription": "[rʌn]", "translation": "Жүгіру", "example": "I run every morning."},
    {"word": "Walk", "transcription": "[wɔːk]", "translation": "Жаяу жүру", "example": "I walk to school."},
    {"word": "Eat", "transcription": "[iːt]", "translation": "Жеу", "example": "I eat breakfast at 8."},
    {"word": "Sleep", "transcription": "[sliːp]", "translation": "Ұйықтау", "example": "I sleep 8 hours a day."},
    {"word": "Read", "transcription": "[riːd]", "translation": "Оқу", "example": "I read every night."},
    {"word": "Write", "transcription": "[raɪt]", "translation": "Жазу", "example": "I write in my diary."},
    {"word": "Listen", "transcription": "[ˈlɪsən]", "translation": "Тыңдау", "example": "Listen to the teacher."},
    {"word": "Speak", "transcription": "[spiːk]", "translation": "Сөйлеу", "example": "I speak English."},
    {"word": "Small", "transcription": "[smɔːl]", "translation": "Кішкентай", "example": "It is a small dog."},
    {"word": "Big", "transcription": "[bɪɡ]", "translation": "Үлкен", "example": "This is a big house."},
    {"word": "Old", "transcription": "[oʊld]", "translation": "Ескі / Қарт", "example": "This is an old book."},
    {"word": "New", "transcription": "[njuː]", "translation": "Жаңа", "example": "I have a new phone."},
    {"word": "Hot", "transcription": "[hɒt]", "translation": "Ыстық", "example": "The tea is hot."},
    {"word": "Cold", "transcription": "[koʊld]", "translation": "Суық", "example": "It is cold outside."},
    {"word": "Fast", "transcription": "[fæst]", "translation": "Жылдам", "example": "He runs fast."},
    {"word": "Slow", "transcription": "[sloʊ]", "translation": "Баяу", "example": "The turtle is slow."},
    {"word": "Yes", "transcription": "[jes]", "translation": "Иә", "example": "Yes, I understand."},
    {"word": "No", "transcription": "[noʊ]", "translation": "Жоқ", "example": "No, I do not agree."},
    {"word": "Please", "transcription": "[pliːz]", "translation": "Өтінемін", "example": "Please help me."},
    # A2 - Elementary
    {"word": "Travel", "transcription": "[ˈtrævəl]", "translation": "Саяхат", "example": "I love to travel."},
    {"word": "Weather", "transcription": "[ˈweðər]", "translation": "Ауа райы", "example": "The weather is nice today."},
    {"word": "Market", "transcription": "[ˈmɑːrkɪt]", "translation": "Базар", "example": "I go to the market on weekends."},
    {"word": "Health", "transcription": "[helθ]", "translation": "Денсаулық", "example": "Health is very important."},
    {"word": "Exercise", "transcription": "[ˈeksərsaɪz]", "translation": "Жаттығу", "example": "I exercise every morning."},
    {"word": "Music", "transcription": "[ˈmjuːzɪk]", "translation": "Музыка", "example": "I listen to music every day."},
    {"word": "Dance", "transcription": "[dæns]", "translation": "Би билеу", "example": "She loves to dance."},
    {"word": "Sing", "transcription": "[sɪŋ]", "translation": "Ән айту", "example": "He sings beautifully."},
    {"word": "Cook", "transcription": "[kʊk]", "translation": "Пісіру", "example": "I cook dinner every evening."},
    {"word": "Clean", "transcription": "[kliːn]", "translation": "Тазалау", "example": "I clean my room every week."},
    {"word": "Buy", "transcription": "[baɪ]", "translation": "Сатып алу", "example": "I want to buy a new book."},
    {"word": "Sell", "transcription": "[sel]", "translation": "Сату", "example": "He sells vegetables."},
    {"word": "Learn", "transcription": "[lɜːrn]", "translation": "Үйрену", "example": "I learn English every day."},
    {"word": "Teach", "transcription": "[tiːtʃ]", "translation": "Үйрету", "example": "She teaches English."},
    {"word": "Help", "transcription": "[help]", "translation": "Көмектесу", "example": "Please help me with this."},
    {"word": "Answer", "transcription": "[ˈænsər]", "translation": "Жауап беру", "example": "Please answer my question."},
    {"word": "Question", "transcription": "[ˈkwestʃən]", "translation": "Сұрақ", "example": "I have a question."},
    {"word": "Problem", "transcription": "[ˈprɒbləm]", "translation": "Мәселе", "example": "We have a small problem."},
    {"word": "Important", "transcription": "[ɪmˈpɔːrtənt]", "translation": "Маңызды", "example": "This is very important."},
    {"word": "Beautiful", "transcription": "[ˈbjuːtɪfəl]", "translation": "Әдемі", "example": "She is very beautiful."},
    {"word": "Strong", "transcription": "[strɒŋ]", "translation": "Күшті", "example": "He is very strong."},
    {"word": "Tired", "transcription": "[ˈtaɪərd]", "translation": "Шаршаған", "example": "I am very tired today."},
    {"word": "Hungry", "transcription": "[ˈhʌŋɡri]", "translation": "Аш", "example": "I am hungry, lets eat."},
    {"word": "Thirsty", "transcription": "[ˈθɜːrsti]", "translation": "Шөлдеген", "example": "I am thirsty, give me water."},
    {"word": "Busy", "transcription": "[ˈbɪzi]", "translation": "Бос емес", "example": "I am very busy today."},
    {"word": "Free", "transcription": "[friː]", "translation": "Бос", "example": "Are you free tonight?"},
    {"word": "Early", "transcription": "[ˈɜːrli]", "translation": "Ерте", "example": "I wake up early."},
    {"word": "Late", "transcription": "[leɪt]", "translation": "Кеш", "example": "Do not be late for school."},
    {"word": "Always", "transcription": "[ˈɔːlweɪz]", "translation": "Әрқашан", "example": "I always drink water."},
    {"word": "Never", "transcription": "[ˈnevər]", "translation": "Ешқашан", "example": "I never eat junk food."},
    {"word": "Sometimes", "transcription": "[ˈsʌmtaɪmz]", "translation": "Кейде", "example": "I sometimes go to the gym."},
    {"word": "Together", "transcription": "[təˈɡeðər]", "translation": "Бірге", "example": "Let us do this together."},
    {"word": "Alone", "transcription": "[əˈloʊn]", "translation": "Жалғыз", "example": "I live alone."},
    {"word": "Ready", "transcription": "[ˈredi]", "translation": "Дайын", "example": "Are you ready to start?"},
    {"word": "Sorry", "transcription": "[ˈsɒri]", "translation": "Кешіріңіз", "example": "I am sorry for being late."},
    {"word": "Thank", "transcription": "[θæŋk]", "translation": "Рахмет айту", "example": "Thank you for your help."},
    {"word": "Welcome", "transcription": "[ˈwelkəm]", "translation": "Қош келдіңіз", "example": "Welcome to our school."},
    {"word": "Understand", "transcription": "[ˌʌndərˈstænd]", "translation": "Түсіну", "example": "Do you understand me?"},
    {"word": "Remember", "transcription": "[rɪˈmembər]", "translation": "Есте сақтау", "example": "Remember to call me."},
    {"word": "Forget", "transcription": "[fərˈɡet]", "translation": "Ұмыту", "example": "Do not forget your keys."},
    {"word": "Start", "transcription": "[stɑːrt]", "translation": "Бастау", "example": "Let us start the lesson."},
    {"word": "Finish", "transcription": "[ˈfɪnɪʃ]", "translation": "Аяқтау", "example": "I finish work at 6."},
    {"word": "Open", "transcription": "[ˈoʊpən]", "translation": "Ашу", "example": "Open the window please."},
    {"word": "Close", "transcription": "[kloʊz]", "translation": "Жабу", "example": "Close the door behind you."},
    {"word": "Give", "transcription": "[ɡɪv]", "translation": "Беру", "example": "Give me the book please."},
    {"word": "Take", "transcription": "[teɪk]", "translation": "Алу", "example": "Take this medicine."},
    {"word": "Come", "transcription": "[kʌm]", "translation": "Келу", "example": "Come here please."},
    {"word": "Go", "transcription": "[ɡoʊ]", "translation": "Кету", "example": "I go to work by bus."},
    {"word": "Find", "transcription": "[faɪnd]", "translation": "Табу", "example": "I cannot find my keys."},
    {"word": "Need", "transcription": "[niːd]", "translation": "Қажет болу", "example": "I need your help."},
    # B1 - Intermediate
    {"word": "Achieve", "transcription": "[əˈtʃiːv]", "translation": "Жету", "example": "You can achieve anything."},
    {"word": "Confident", "transcription": "[ˈkɒnfɪdənt]", "translation": "Сенімді", "example": "She is very confident."},
    {"word": "Challenge", "transcription": "[ˈtʃælɪndʒ]", "translation": "Қиындық", "example": "Every challenge makes you stronger."},
    {"word": "Opportunity", "transcription": "[ˌɒpəˈtjuːnɪti]", "translation": "Мүмкіндік", "example": "Do not miss this opportunity."},
    {"word": "Experience", "transcription": "[ɪkˈspɪəriəns]", "translation": "Тәжірибе", "example": "Experience is the best teacher."},
    {"word": "Knowledge", "transcription": "[ˈnɒlɪdʒ]", "translation": "Білім", "example": "Knowledge is power."},
    {"word": "Success", "transcription": "[səkˈses]", "translation": "Жетістік", "example": "Hard work leads to success."},
    {"word": "Failure", "transcription": "[ˈfeɪljər]", "translation": "Сәтсіздік", "example": "Failure is a part of learning."},
    {"word": "Improve", "transcription": "[ɪmˈpruːv]", "translation": "Жақсарту", "example": "I want to improve my English."},
    {"word": "Develop", "transcription": "[dɪˈveləp]", "translation": "Дамыту", "example": "We need to develop new skills."},
    {"word": "Decision", "transcription": "[dɪˈsɪʒən]", "translation": "Шешім", "example": "Make a wise decision."},
    {"word": "Responsibility", "transcription": "[rɪˌspɒnsɪˈbɪlɪti]", "translation": "Жауапкершілік", "example": "Take responsibility for your actions."},
    {"word": "Honest", "transcription": "[ˈɒnɪst]", "translation": "Адал", "example": "Always be honest."},
    {"word": "Creative", "transcription": "[kriˈeɪtɪv]", "translation": "Шығармашыл", "example": "She is very creative."},
    {"word": "Curious", "transcription": "[ˈkjʊəriəs]", "translation": "Қызығушылықты", "example": "Be curious about the world."},
    {"word": "Generous", "transcription": "[ˈdʒenərəs]", "translation": "Жомарт", "example": "He is very generous."},
    {"word": "Kindness", "transcription": "[ˈkaɪndnəs]", "translation": "Мейірімділік", "example": "Kindness costs nothing."},
    {"word": "Respect", "transcription": "[rɪˈspekt]", "translation": "Құрмет", "example": "Respect your elders."},
    {"word": "Trust", "transcription": "[trʌst]", "translation": "Сену", "example": "Trust is very important."},
    {"word": "Support", "transcription": "[səˈpɔːrt]", "translation": "Қолдау", "example": "I support my family."},
    {"word": "Manage", "transcription": "[ˈmænɪdʒ]", "translation": "Басқару", "example": "I manage a small team."},
    {"word": "Solve", "transcription": "[sɒlv]", "translation": "Шешу", "example": "We need to solve this problem."},
    {"word": "Suggest", "transcription": "[səˈdʒest]", "translation": "Ұсыну", "example": "I suggest we meet tomorrow."},
    {"word": "Explain", "transcription": "[ɪkˈspleɪn]", "translation": "Түсіндіру", "example": "Can you explain this to me?"},
    {"word": "Describe", "transcription": "[dɪˈskraɪb]", "translation": "Сипаттау", "example": "Describe what you see."},
    {"word": "Compare", "transcription": "[kəmˈpeər]", "translation": "Салыстыру", "example": "Compare these two options."},
    {"word": "Consider", "transcription": "[kənˈsɪdər]", "translation": "Ойластыру", "example": "Consider all the options."},
    {"word": "Prepare", "transcription": "[prɪˈpeər]", "translation": "Дайындалу", "example": "Prepare for the exam."},
    {"word": "Organize", "transcription": "[ˈɔːrɡənaɪz]", "translation": "Ұйымдастыру", "example": "Organize your time well."},
    {"word": "Communicate", "transcription": "[kəˈmjuːnɪkeɪt]", "translation": "Қарым-қатынас жасау", "example": "Communicate clearly."},
    {"word": "Motivate", "transcription": "[ˈmoʊtɪveɪt]", "translation": "Ынталандыру", "example": "Motivate yourself every day."},
    {"word": "Celebrate", "transcription": "[ˈselɪbreɪt]", "translation": "Тойлау", "example": "Let us celebrate your success."},
    {"word": "Appreciate", "transcription": "[əˈpriːʃieɪt]", "translation": "Бағалау", "example": "I appreciate your help."},
    {"word": "Encourage", "transcription": "[ɪnˈkʌrɪdʒ]", "translation": "Батылдандыру", "example": "Encourage others to do better."},
    {"word": "Inspire", "transcription": "[ɪnˈspaɪər]", "translation": "Шабыттандыру", "example": "She inspires everyone around her."},
    {"word": "Adapt", "transcription": "[əˈdæpt]", "translation": "Бейімделу", "example": "Adapt to new situations."},
    {"word": "Focus", "transcription": "[ˈfoʊkəs]", "translation": "Шоғырлану", "example": "Focus on your goals."},
    {"word": "Dedicate", "transcription": "[ˈdedɪkeɪt]", "translation": "Арнау", "example": "Dedicate time to learning."},
    {"word": "Persist", "transcription": "[pəˈsɪst]", "translation": "Табандылық таныту", "example": "Persist even when it is hard."},
    {"word": "Balance", "transcription": "[ˈbæləns]", "translation": "Тепе-теңдік", "example": "Balance work and rest."},
    {"word": "Positive", "transcription": "[ˈpɒzɪtɪv]", "translation": "Оң", "example": "Stay positive always."},
    {"word": "Negative", "transcription": "[ˈneɡətɪv]", "translation": "Теріс", "example": "Avoid negative thoughts."},
    {"word": "Attitude", "transcription": "[ˈætɪtjuːd]", "translation": "Көзқарас", "example": "Your attitude determines your success."},
    {"word": "Habit", "transcription": "[ˈhæbɪt]", "translation": "Әдет", "example": "Build good habits daily."},
    {"word": "Goal", "transcription": "[ɡoʊl]", "translation": "Мақсат", "example": "Set clear goals for yourself."},
    {"word": "Plan", "transcription": "[plæn]", "translation": "Жоспар", "example": "Make a plan before you start."},
    {"word": "Progress", "transcription": "[ˈprəʊɡres]", "translation": "Прогресс", "example": "Track your progress daily."},
    {"word": "Effort", "transcription": "[ˈefərt]", "translation": "Күш-жігер", "example": "Put effort into everything."},
    {"word": "Result", "transcription": "[rɪˈzʌlt]", "translation": "Нәтиже", "example": "Hard work gives good results."},
    {"word": "Value", "transcription": "[ˈvæljuː]", "translation": "Құндылық", "example": "Value your time and energy."},
    # B2 - Upper-Intermediate
    {"word": "Resilience", "transcription": "[rɪˈzɪliəns]", "translation": "Төзімділік", "example": "Resilience helps you overcome obstacles."},
    {"word": "Ambition", "transcription": "[æmˈbɪʃən]", "translation": "Амбиция", "example": "Ambition drives people to succeed."},
    {"word": "Integrity", "transcription": "[ɪnˈteɡrɪti]", "translation": "Адалдық", "example": "Integrity is the foundation of trust."},
    {"word": "Perseverance", "transcription": "[ˌpɜːrsɪˈvɪərəns]", "translation": "Табандылық", "example": "Perseverance leads to success."},
    {"word": "Discipline", "transcription": "[ˈdɪsɪplɪn]", "translation": "Тәртіп", "example": "Discipline is the key to achievement."},
    {"word": "Empathy", "transcription": "[ˈempəθi]", "translation": "Жанашырлық", "example": "Empathy connects people deeply."},
    {"word": "Innovation", "transcription": "[ˌɪnəˈveɪʃən]", "translation": "Инновация", "example": "Innovation drives progress."},
    {"word": "Leadership", "transcription": "[ˈliːdərʃɪp]", "translation": "Көшбасшылық", "example": "Good leadership inspires teams."},
    {"word": "Collaboration", "transcription": "[kəˌlæbəˈreɪʃən]", "translation": "Ынтымақтастық", "example": "Collaboration leads to better results."},
    {"word": "Commitment", "transcription": "[kəˈmɪtmənt]", "translation": "Міндеттеме", "example": "Show commitment to your work."},
    {"word": "Transparency", "transcription": "[trænsˈpærənsi]", "translation": "Ашықтық", "example": "Transparency builds trust."},
    {"word": "Accountability", "transcription": "[əˌkaʊntəˈbɪlɪti]", "translation": "Есеп беру", "example": "Take accountability for your actions."},
    {"word": "Sustainability", "transcription": "[səˌsteɪnəˈbɪlɪti]", "translation": "Тұрақтылық", "example": "Sustainability is important for the future."},
    {"word": "Diversity", "transcription": "[daɪˈvɜːrsɪti]", "translation": "Алуантүрлілік", "example": "Diversity makes teams stronger."},
    {"word": "Compassion", "transcription": "[kəmˈpæʃən]", "translation": "Мейірім", "example": "Show compassion to others."},
    {"word": "Determination", "transcription": "[dɪˌtɜːrmɪˈneɪʃən]", "translation": "Қажырлылық", "example": "Determination helps you reach your goals."},
    {"word": "Flexibility", "transcription": "[ˌfleksɪˈbɪlɪti]", "translation": "Икемділік", "example": "Flexibility is key in business."},
    {"word": "Productivity", "transcription": "[ˌprɒdʌkˈtɪvɪti]", "translation": "Өнімділік", "example": "Increase your productivity daily."},
    {"word": "Creativity", "transcription": "[ˌkriːeɪˈtɪvɪti]", "translation": "Шығармашылық", "example": "Creativity solves problems."},
    {"word": "Mindfulness", "transcription": "[ˈmaɪndfʊlnəs]", "translation": "Зейінділік", "example": "Practice mindfulness every day."},
    {"word": "Gratitude", "transcription": "[ˈɡrætɪtjuːd]", "translation": "Алғыс", "example": "Gratitude improves your mood."},
    {"word": "Optimism", "transcription": "[ˈɒptɪmɪzəm]", "translation": "Оптимизм", "example": "Optimism helps you move forward."},
    {"word": "Enthusiasm", "transcription": "[ɪnˈθjuːziæzəm]", "translation": "Ынта", "example": "Approach work with enthusiasm."},
    {"word": "Authenticity", "transcription": "[ˌɔːθenˈtɪsɪti]", "translation": "Шынайылық", "example": "Be authentic in everything you do."},
    {"word": "Vulnerability", "transcription": "[ˌvʌlnərəˈbɪlɪti]", "translation": "Осалдық", "example": "Showing vulnerability takes courage."},
    {"word": "Consequence", "transcription": "[ˈkɒnsɪkwəns]", "translation": "Салдар", "example": "Think about the consequences."},
    {"word": "Perspective", "transcription": "[pəˈspektɪv]", "translation": "Көзқарас", "example": "Change your perspective."},
    {"word": "Influence", "transcription": "[ˈɪnfluəns]", "translation": "Ықпал", "example": "You have a positive influence."},
    {"word": "Momentum", "transcription": "[moʊˈmentəm]", "translation": "Серпін", "example": "Keep the momentum going."},
    {"word": "Overcome", "transcription": "[ˌoʊvərˈkʌm]", "translation": "Жеңу", "example": "Overcome your fears."},
    {"word": "Thrive", "transcription": "[θraɪv]", "translation": "Өркендеу", "example": "Thrive in every situation."},
    {"word": "Flourish", "transcription": "[ˈflʌrɪʃ]", "translation": "Гүлдену", "example": "Let your talent flourish."},
    {"word": "Elevate", "transcription": "[ˈelɪveɪt]", "translation": "Жоғарылату", "example": "Elevate your standards."},
    {"word": "Empower", "transcription": "[ɪmˈpaʊər]", "translation": "Күш беру", "example": "Empower others to grow."},
    {"word": "Prioritize", "transcription": "[praɪˈɒrɪtaɪz]", "translation": "Басымдық беру", "example": "Prioritize your health."},
    {"word": "Strategize", "transcription": "[ˈstrætɪdʒaɪz]", "translation": "Стратегия жасау", "example": "Strategize before you act."},
    {"word": "Visualize", "transcription": "[ˈvɪʒuəlaɪz]", "translation": "Елестету", "example": "Visualize your success."},
    {"word": "Implement", "transcription": "[ˈɪmplɪment]", "translation": "Іске асыру", "example": "Implement your plan today."},
    {"word": "Evaluate", "transcription": "[ɪˈvæljueɪt]", "translation": "Бағалау", "example": "Evaluate your progress weekly."},
    {"word": "Transform", "transcription": "[trænsˈfɔːrm]", "translation": "Өзгерту", "example": "Transform your life with good habits."},
    {"word": "Invest", "transcription": "[ɪnˈvest]", "translation": "Инвестиция салу", "example": "Invest in yourself first."},
    {"word": "Leverage", "transcription": "[ˈlevərɪdʒ]", "translation": "Пайдалану", "example": "Leverage your strengths."},
    {"word": "Cultivate", "transcription": "[ˈkʌltɪveɪt]", "translation": "Дамыту", "example": "Cultivate good relationships."},
    {"word": "Nurture", "transcription": "[ˈnɜːrtʃər]", "translation": "Тәрбиелеу", "example": "Nurture your talents."},
    {"word": "Sustain", "transcription": "[səˈsteɪn]", "translation": "Қолдау", "example": "Sustain your efforts over time."},
    {"word": "Acknowledge", "transcription": "[əkˈnɒlɪdʒ]", "translation": "Мойындау", "example": "Acknowledge your mistakes."},
    {"word": "Embrace", "transcription": "[ɪmˈbreɪs]", "translation": "Қабылдау", "example": "Embrace change with open arms."},
    {"word": "Navigate", "transcription": "[ˈnævɪɡeɪt]", "translation": "Бағдарлау", "example": "Navigate through challenges."},
    {"word": "Articulate", "transcription": "[ɑːrˈtɪkjuleɪt]", "translation": "Нақты айту", "example": "Articulate your ideas clearly."},
    {"word": "Reflect", "transcription": "[rɪˈflekt]", "translation": "Ойлану", "example": "Reflect on your experiences."},
    {"word": "Evolve", "transcription": "[ɪˈvɒlv]", "translation": "Дамыту", "example": "Evolve your thinking constantly."},
    # C1 - Advanced
    {"word": "Tenacity", "transcription": "[tɪˈnæsɪti]", "translation": "Қажырлылық", "example": "Tenacity is the mark of a true leader."},
    {"word": "Eloquence", "transcription": "[ˈeləkwəns]", "translation": "Шешендік", "example": "Her eloquence impressed everyone."},
    {"word": "Pragmatic", "transcription": "[præɡˈmætɪk]", "translation": "Прагматикалық", "example": "Be pragmatic in your approach."},
    {"word": "Meticulous", "transcription": "[mɪˈtɪkjələs]", "translation": "Мұқият", "example": "He is meticulous in his work."},
    {"word": "Profound", "transcription": "[prəˈfaʊnd]", "translation": "Терең", "example": "She has a profound understanding."},
    {"word": "Intrinsic", "transcription": "[ɪnˈtrɪnsɪk]", "translation": "Ішкі", "example": "Find intrinsic motivation."},
    {"word": "Paradigm", "transcription": "[ˈpærədaɪm]", "translation": "Парадигма", "example": "Shift your paradigm."},
    {"word": "Synergy", "transcription": "[ˈsɪnərdʒi]", "translation": "Синергия", "example": "Create synergy within your team."},
    {"word": "Acumen", "transcription": "[ˈækjʊmən]", "translation": "Тапқырлық", "example": "Business acumen is essential."},
    {"word": "Astute", "transcription": "[əˈstjuːt]", "translation": "Зерек", "example": "She is an astute businesswoman."},
    {"word": "Candid", "transcription": "[ˈkændɪd]", "translation": "Ашық", "example": "Be candid about your feelings."},
    {"word": "Cohesive", "transcription": "[koʊˈhiːsɪv]", "translation": "Тұтас", "example": "Build a cohesive team."},
    {"word": "Diligence", "transcription": "[ˈdɪlɪdʒəns]", "translation": "Ынта", "example": "Diligence always pays off."},
    {"word": "Erudite", "transcription": "[ˈerʊdaɪt]", "translation": "Білімді", "example": "He is an erudite scholar."},
    {"word": "Fortitude", "transcription": "[ˈfɔːrtɪtjuːd]", "translation": "Ерлік", "example": "Face challenges with fortitude."},
    {"word": "Gregarious", "transcription": "[ɡrɪˈɡeəriəs]", "translation": "Жайдары", "example": "She is very gregarious."},
    {"word": "Humility", "transcription": "[hjuːˈmɪlɪti]", "translation": "Кішіпейілділік", "example": "Humility is a great virtue."},
    {"word": "Impeccable", "transcription": "[ɪmˈpekəbəl]", "translation": "Мінсіз", "example": "Her work is impeccable."},
    {"word": "Judicious", "transcription": "[dʒuːˈdɪʃəs]", "translation": "Ақылды", "example": "Make judicious decisions."},
    {"word": "Lucid", "transcription": "[ˈluːsɪd]", "translation": "Анық", "example": "Give a lucid explanation."},
    {"word": "Magnanimous", "transcription": "[mæɡˈnænɪməs]", "translation": "Кең пейілді", "example": "Be magnanimous in victory."},
    {"word": "Nuanced", "transcription": "[ˈnjuːɑːnst]", "translation": "Нюансты", "example": "A nuanced understanding is needed."},
    {"word": "Objective", "transcription": "[əbˈdʒektɪv]", "translation": "Объективті", "example": "Stay objective in your analysis."},
    {"word": "Perceptive", "transcription": "[pəˈseptɪv]", "translation": "Зейінді", "example": "She is very perceptive."},
    {"word": "Resolute", "transcription": "[ˈrezəluːt]", "translation": "Табанды", "example": "Be resolute in your decisions."},
    {"word": "Scrupulous", "transcription": "[ˈskruːpjələs]", "translation": "Адал", "example": "Be scrupulous in your dealings."},
    {"word": "Tenacious", "transcription": "[tɪˈneɪʃəs]", "translation": "Жігерлі", "example": "Be tenacious in pursuing your dreams."},
    {"word": "Altruistic", "transcription": "[ˌæltruˈɪstɪk]", "translation": "Жомарт", "example": "Altruistic people help others."},
    {"word": "Benevolent", "transcription": "[bɪˈnevələnt]", "translation": "Қайырымды", "example": "A benevolent leader cares for others."},
    {"word": "Conscientious", "transcription": "[ˌkɒnʃiˈenʃəs]", "translation": "Ұждандылық", "example": "Be conscientious in your work."},
    {"word": "Discerning", "transcription": "[dɪˈsɜːrnɪŋ]", "translation": "Зерек", "example": "A discerning eye sees the details."},
    {"word": "Exemplary", "transcription": "[ɪɡˈzempləri]", "translation": "Үлгілі", "example": "Show exemplary behavior."},
    {"word": "Forthright", "transcription": "[ˈfɔːrθraɪt]", "translation": "Тікелей", "example": "Be forthright in your communication."},
    {"word": "Inquisitive", "transcription": "[ɪnˈkwɪzɪtɪv]", "translation": "Зерттегіш", "example": "Stay inquisitive and keep learning."},
    {"word": "Luminous", "transcription": "[ˈluːmɪnəs]", "translation": "Жарқын", "example": "She has a luminous personality."},
    {"word": "Perspicacious", "transcription": "[ˌpɜːrspɪˈkeɪʃəs]", "translation": "Аңғарымпаз", "example": "A perspicacious leader sees the future."},
    {"word": "Sagacious", "transcription": "[səˈɡeɪʃəs]", "translation": "Дана", "example": "A sagacious leader listens well."},
    {"word": "Transcend", "transcription": "[trænˈsend]", "translation": "Асып түсу", "example": "Transcend your limitations."},
    {"word": "Unwavering", "transcription": "[ʌnˈweɪvərɪŋ]", "translation": "Тұрақты", "example": "Show unwavering commitment."},
    {"word": "Venerate", "transcription": "[ˈvenəreɪt]", "translation": "Құрмет тұту", "example": "Venerate wisdom and experience."},
    {"word": "Wholesome", "transcription": "[ˈhoʊlsəm]", "translation": "Пайдалы", "example": "Lead a wholesome lifestyle."},
    {"word": "Zealous", "transcription": "[ˈzeləs]", "translation": "Ынтазар", "example": "Be zealous about your goals."},
    {"word": "Unequivocal", "transcription": "[ˌʌnɪˈkwɪvəkəl]", "translation": "Анық", "example": "Give an unequivocal answer."},
    {"word": "Veracious", "transcription": "[vəˈreɪʃəs]", "translation": "Шынайы", "example": "A veracious person always tells truth."},
    {"word": "Wisdom", "transcription": "[ˈwɪzdəm]", "translation": "Даналық", "example": "Wisdom grows with experience."},
    {"word": "Xenial", "transcription": "[ˈziːniəl]", "translation": "Қонақжай", "example": "Be xenial to all your guests."},
    {"word": "Authentic", "transcription": "[ɔːˈθentɪk]", "translation": "Шынайы", "example": "Be authentic in all you do."},
    {"word": "Catalyze", "transcription": "[ˈkætəlaɪz]", "translation": "Жеделдету", "example": "Catalyze positive change."},
    {"word": "Diligent", "transcription": "[ˈdɪlɪdʒənt]", "translation": "Ынталы", "example": "Be diligent in your studies."},
    {"word": "Eminent", "transcription": "[ˈemɪnənt]", "translation": "Көрнекті", "example": "He is an eminent scholar."},
    {"word": "Foresight", "transcription": "[ˈfɔːrsaɪt]", "translation": "Болжау", "example": "Good leaders have great foresight."},
]

logging.basicConfig(level=logging.INFO)
day_counter = {"index": 0}

def get_three_words():
    idx = day_counter["index"] % (len(WORDS) // 3)
    trio = WORDS[idx * 3: idx * 3 + 3]
    day_counter["index"] += 1
    return trio

async def send_daily_words(context: ContextTypes.DEFAULT_TYPE):
    words = get_three_words()
    message = "🌟 *ABA Group — Күнделікті ағылшын сөздері*\n\n"
    for i, w in enumerate(words, 1):
        message += f"*{i}. {w['word']}* {w['transcription']} — _{w['translation']}_\n"
        message += f"📝 {w['example']}\n"
        message += f"🔊 forvo.com/word/{w['word'].lower()}\n\n"
    message += "💪 Осы сөздерді бүгін қолданып көріңіз!"
    await context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Сәлем! Мен *ABA Group English* боты!\n\n"
        "📚 A1-ден C1-ге дейін 250 ағылшын сөзін үйренесіз!\n"
        "⏰ Күн сайын таңертең 3 жаңа сөз келеді.\n\n"
        "/words — қазір сөз алу\n"
        "/level — деңгейлер туралы",
        parse_mode="Markdown"
    )

async def words_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words = get_three_words()
    message = "🌟 *ABA Group — Күнделікті ағылшын сөздері*\n\n"
    for i, w in enumerate(words, 1):
        message += f"*{i}. {w['word']}* {w['transcription']} — _{w['translation']}_\n"
        message += f"📝 {w['example']}\n"
        message += f"🔊 forvo.com/word/{w['word'].lower()}\n\n"
    await update.message.reply_text(message, parse_mode="Markdown")

async def level_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "📊 *Деңгейлер:*\n\n"
        "🟢 *A1* — Beginner (50 сөз)\n"
        "🔵 *A2* — Elementary (50 сөз)\n"
        "🟡 *B1* — Intermediate (50 сөз)\n"
        "🟠 *B2* — Upper-Intermediate (50 сөз)\n"
        "🔴 *C1* — Advanced (50 сөз)\n\n"
        "Барлығы: *250 сөз* — 83 күн!"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("words", words_now))
    app.add_handler(CommandHandler("level", level_info))
    app.job_queue.run_daily(send_daily_words, time=time(hour=4, minute=0))
    app.run_polling()

if __name__ == "__main__":
    main()
