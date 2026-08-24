import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai

# .env файлынан API Key оқу
load_dotenv()
# Прогресті сақтау функциясы
PROGRESS_FILE = "progress.json"
PLAN_FILE = "study_plan.json"


def save_progress(score, percentage):
    progress = {
        "tests_completed": st.session_state.get("tests_completed", 0),
        "last_score": score,
        "last_percentage": percentage
    }

    with open(PROGRESS_FILE, "w", encoding="utf-8") as file:
        json.dump(progress, file, ensure_ascii=False, indent=4)
def save_study_plan(plan):
    with open(PLAN_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"study_plan": plan},
            file,
            ensure_ascii=False,
            indent=4
        )

API_KEY = os.getenv("GEMINI_API_KEY")
# Сақталған прогресті жүктеу
if os.path.exists(PROGRESS_FILE):
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as file:
            saved_progress = json.load(file)

        st.session_state.tests_completed = saved_progress.get(
            "tests_completed", 0
        )

        st.session_state.last_score = saved_progress.get(
            "last_score", 0
        )

        st.session_state.last_percentage = saved_progress.get(
            "last_percentage", 0
        )

    except Exception:
        pass
# Сақталған оқу жоспарын жүктеу
if os.path.exists(PLAN_FILE):
    try:
        with open(PLAN_FILE, "r", encoding="utf-8") as file:
            saved_plan = json.load(file)

        st.session_state.study_plan = saved_plan.get(
            "study_plan", ""
        )

    except Exception:
        pass

# Gemini клиентін қосу
if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None

# Бет баптаулары
st.set_page_config(
    page_title="AI Репетитор",
    page_icon="🤖",
    layout="wide"
)
# Интерфейс дизайны
st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: visible;
}

/* Негізгі тақырып */
h1 {
    font-weight: 700;
}

/* Бөлім тақырыптары */
h2, h3 {
    font-weight: 600;
}

/* Батырмалар */
.stButton > button {
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
}

/* Ақпараттық блоктар */
.stAlert {
    border-radius: 10px;
}

/* Мәзір */
section[data-testid="stSidebar"] {
    border-right: 1px solid #e5e7eb;
}

/* Карточкалар */
div[data-testid="stMetric"] {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)# Тақырып
st.title("🤖 AI Репетитор")
st.write("Жасанды интеллект негізіндегі репетитор")
st.sidebar.title("📚 МӘЗІР")

page = st.sidebar.selectbox(
    "Бөлімді таңдаңыз",
    [
        "🏠 Басты бет",
        "🤖 AI Репетитор",
        "📖 Сабақтар",
        "📝 Тесттер",
        "📊 Оқу үлгерімі",
        "📅 Жеке оқу жоспары"
    ]
)
# Басты бет
if page == "🏠 Басты бет":

    st.header("AI Репетиторға қош келдіңіз!")

    st.write(
        "Жеке оқу, түсіндіру және білімді тексеруге арналған "
        "жасанды интеллект жүйесі."
    )

    st.divider()

    st.subheader("Жүйенің мүмкіндіктері")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🤖 Жеке репетитор")
        st.write(
            "Сұрақтарыңызға жауап алыңыз және "
            "тақырыптарды қарапайым тілмен түсініңіз."
        )

    with col2:
        st.markdown("### 📖 Сабақтар")
        st.write(
            "Пән мен тақырыпты таңдап, "
            "жеке түсіндірме сабақ алыңыз."
        )

    with col3:
        st.markdown("### 📝 Тесттер")
        st.write(
            "Біліміңізді тексеріп, "
            "автоматты түрде нәтиже алыңыз."
        )

    st.divider()

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("### 📊 Оқу үлгерімі")
        st.write(
            "Тест нәтижелеріңізді бақылап, "
            "оқу прогресіңізді көріңіз."
        )

    with col5:
        st.markdown("### 📅 Жеке оқу жоспары")
        st.write(
            "Мақсатыңызға сәйкес "
            "жеке оқу жоспарын құрыңыз."
        )

    with col6:
        st.markdown("### 🎓 Оқу деңгейі")
        st.write(
            "Өз деңгейіңізге сәйкес "
            "оқу материалдарын пайдаланыңыз."
        )

    st.divider()

    st.subheader("Жұмысты бастау")

    st.info(
        "Сол жақтағы мәзірден қажетті бөлімді таңдаңыз. "
        "Сабақ оқып, тест тапсырып, нәтижелеріңізді бақылаңыз."
    )
# AI Репетитор
elif page == "🤖 AI Репетитор":
    st.header("🤖 AI Репетитор")

    if not API_KEY:
        st.error("Gemini API Key табылмады. .env файлын тексеріңіз.")
    else:
        st.success("Gemini AI қосылды ✅")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Бұрынғы хабарламаларды көрсету
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Оқушының сұрағы
        prompt = st.chat_input("Сұрағыңызды жазыңыз...")

        if prompt:
            # Оқушы хабарламасы
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            with st.chat_message("user"):
                st.markdown(prompt)

            # AI жауабы
            with st.chat_message("assistant"):
                with st.spinner("AI ойланып жатыр..."):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.6-flash",
                            contents=prompt
                        )

                        answer = response.text
                        st.markdown(answer)

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": answer
                            }
                        )

                    except Exception as e:
                        st.exception(e)
# Сабақ
elif page == "📖 Сабақтар":
    st.header("📚 AI Сабақ")

    st.write("Пән мен тақырыпты таңдаңыз. AI сізге тақырыпты түсіндіреді.")

    subject = st.selectbox(
        "📚 Пәнді таңдаңыз",
        [
            "Информатика",
            "Математика",
            "Қазақ тілі",
            "Ағылшын тілі",
            "Физика"
        ]
    )

    topic = st.text_input(
        "📝 Сабақ тақырыбы",
        placeholder="Мысалы: Python-дағы циклдер"
    )

    level = st.selectbox(
        "🎓 Деңгей",
        [
            "Бастапқы",
            "Орта",
            "Жоғары"
        ]
    )

    if st.button("📖 Сабақты түсіндіру"):
        if not topic:
            st.warning("Алдымен сабақ тақырыбын жазыңыз.")
        else:
            with st.spinner("AI сабақ дайындап жатыр..."):
                try:
                    lesson_prompt = f"""
Сен оқушыға арналған AI Репетиторсың.

Пән: {subject}
Тақырып: {topic}
Оқушы деңгейі: {level}

Осы тақырып бойынша түсінікті сабақ дайында.

Мына құрылымды сақта:

1. Сабақтың мақсаты
2. Тақырыпты қарапайым тілмен түсіндіру
3. Негізгі ұғымдар
4. Мысалдар
5. Қадамдық түсіндіру
6. Оқушыға арналған 3 сұрақ
7. Қысқаша қорытынды

Жауапты қазақ тілінде бер.
Оқушының деңгейіне сәйкес түсіндір.
"""

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=lesson_prompt
                    )

                    st.markdown("## 📖 Сабақ")
                    st.markdown(response.text)

                except Exception as e:
                    st.exception(e)# Тест
# Тест
elif page == "📝 Тесттер":
    st.header("📝 AI Тест")

    st.write(
        "Пән мен тақырыпты таңдаңыз. "
        "AI 5 сұрақтан тұратын тест дайындайды."
    )

    subject = st.selectbox(
        "📚 Пәнді таңдаңыз",
        [
            "Информатика",
            "Математика",
            "Қазақ тілі",
            "Ағылшын тілі",
            "Физика"
        ]
    )

    topic = st.text_input(
        "📝 Тақырыпты енгізіңіз",
        placeholder="Мысалы: Python циклдері"
    )

    level = st.selectbox(
        "🎓 Деңгейіңіз",
        [
            "Бастапқы",
            "Орта",
            "Жоғары"
        ]
    )

    if st.button("📝 Тест құру"):

        if not topic:
            st.warning("Алдымен тақырыпты енгізіңіз.")

        elif not API_KEY:
            st.error("Gemini API Key табылмады.")

        else:
            with st.spinner("AI тест дайындап жатыр..."):

                try:
                    test_prompt = f"""
Сен мектеп оқушыларына арналған AI мұғалімсің.

Пән: {subject}
Тақырып: {topic}
Деңгей: {level}

5 тест сұрағын жаса.

Әр сұрақта дәл 4 жауап нұсқасы болсын.

Жауапты тек мына JSON форматында бер:

[
  {{
    "question": "Сұрақ",
    "options": [
      "A) бірінші жауап",
      "B) екінші жауап",
      "C) үшінші жауап",
      "D) төртінші жауап"
    ],
    "answer": "A"
  }}
]

Маңызды:
- Дәл 5 сұрақ болсын.
- Әр сұрақта 4 жауап болсын.
- answer тек A, B, C немесе D болсын.
- Қазақ тілінде жаз.
- JSON-нан басқа ештеңе жазба.
"""

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=test_prompt
                    )

                    text = response.text.strip()

                    if text.startswith("```"):
                        text = text.replace("```json", "")
                        text = text.replace("```", "")
                        text = text.strip()

                    test_data = json.loads(text)

                    st.session_state.test_data = test_data
                    st.session_state.test_topic = topic
                    st.session_state.test_answers = {}

                    st.success("Тест дайын! ✅")

                except Exception as e:
                    st.error("Тестті құру кезінде қате пайда болды.")
                    st.exception(e)

    if "test_data" in st.session_state:

        st.divider()
        st.subheader("📋 Тест")

        test_data = st.session_state.test_data

        for i, question in enumerate(test_data):

            st.write(
                f"### {i + 1}. {question['question']}"
            )

            answer = st.radio(
                "Жауабыңызды таңдаңыз:",
                question["options"],
                index=None,
                key=f"question_{i}"
            )

            if answer is not None:
                st.session_state.test_answers[i] = answer[0]

        st.divider()

        if st.button("✅ Тестті тексеру"):

            unanswered = []

            for i in range(len(test_data)):
                if i not in st.session_state.test_answers:
                    unanswered.append(i + 1)

            if unanswered:

                st.warning(
                    f"⚠️ Жауап берілмеген сұрақтар: "
                    f"{', '.join(map(str, unanswered))}"
                )

            else:

                score = 0

                for i, question in enumerate(test_data):

                    user_answer = st.session_state.test_answers[i]
                    correct_answer = question["answer"]

                    if user_answer == correct_answer:
                        score += 1

                percentage = score * 20

                st.session_state.last_score = score
                st.session_state.last_percentage = percentage

                st.session_state.tests_completed = (
                    st.session_state.get("tests_completed", 0) + 1
                )

                # Нәтижені файлға сақтау
                save_progress(score, percentage)

                st.subheader("📊 Нәтиже")

                st.metric(
                    "Сіздің нәтижеңіз",
                    f"{score}/5"
                )

                st.progress(percentage / 100)

                st.write(
                    f"**Нәтиже: {percentage}%**"
                )

                if percentage == 100:
                    st.success(
                        "🏆 Керемет! Барлық сұрақ дұрыс!"
                    )

                elif percentage >= 80:
                    st.success(
                        "🎉 Өте жақсы нәтиже!"
                    )

                elif percentage >= 60:
                    st.info(
                        "👍 Жақсы нәтиже!"
                    )

                else:
                    st.warning(
                        "📚 Тақырыпты қайта қарап шыққан дұрыс."
                    )

                st.divider()

                st.subheader("🔍 Жауаптарды тексеру")

                for i, question in enumerate(test_data):

                    user_answer = st.session_state.test_answers[i]
                    correct_answer = question["answer"]

                    if user_answer == correct_answer:
                        st.success(
                            f"{i + 1}-сұрақ: Дұрыс ✅"
                        )
                    else:
                        st.error(
                            f"{i + 1}-сұрақ: Қате ❌ "
                            f"(Дұрыс жауап: {correct_answer})"
                        )
# Прогресс
elif page == "📊 Оқу үлгерімі":
    st.header("📊 Менің оқу прогресім")

    # Нәтижелерді алу
    tests_completed = st.session_state.get("tests_completed", 0)
    last_score = st.session_state.get("last_score", 0)
    last_percentage = st.session_state.get("last_percentage", 0)

    # Негізгі статистика
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📝 Тесттер",
            tests_completed
        )

    with col2:
        st.metric(
            "⭐ Соңғы балл",
            f"{last_score}/5"
        )

    with col3:
        st.metric(
            "🎯 Нәтиже",
            f"{last_percentage}%"
        )

    with col4:
        if last_percentage >= 80:
            level_text = "Жоғары"
        elif last_percentage >= 60:
            level_text = "Орта"
        elif last_percentage > 0:
            level_text = "Бастапқы"
        else:
            level_text = "—"

        st.metric(
            "📈 Деңгей",
            level_text
        )

    st.divider()

    # Прогресс шкаласы
    st.subheader("🎯 Жалпы оқу прогресі")

    st.progress(last_percentage / 100)

    if last_percentage == 0:
        st.info(
            "📚 Тест тапсырып бастаңыз. "
            "Сіздің оқу прогресіңіз осы жерде көрсетіледі."
        )

    elif last_percentage >= 80:
        st.success(
            "🏆 Өте жақсы нәтиже! "
            "Оқу қарқыныңыз жақсы."
        )

    elif last_percentage >= 60:
        st.info(
            "👍 Жақсы нәтиже. "
            "Тағы бірнеше тапсырма орындап көріңіз."
        )

    else:
        st.warning(
            "📖 Тақырыптарды тағы бір рет қайталап, "
            "тестті қайта орындап көріңіз."
        )

    st.divider()
#Оқу белсенділігі
    st.subheader("📚 Оқу белсенділігі")

    activity_col1, activity_col2 = st.columns(2)

    with activity_col1:
        st.write("### 📝 Тест нәтижесі")

        if tests_completed > 0:
            st.write(
                f"Орындалған тесттер: **{tests_completed}**"
            )
            st.write(
                f"Соңғы нәтиже: **{last_score}/5**"
            )
        else:
            st.write("Әзірге тест нәтижесі жоқ.")

    with activity_col2:
        st.write("### 🎓 Оқу деңгейі")

        if last_percentage >= 80:
            st.success("Жоғары деңгей")
        elif last_percentage >= 60:
            st.info("Орта деңгей")
        elif last_percentage > 0:
            st.warning("Бастапқы деңгей")
        else:
            st.write("Деңгей анықталмаған.")

    st.divider()

    # Келесі қадам
    st.subheader("🚀 Келесі қадам")

    if last_percentage >= 80:
        st.write(
            "Жаңа тақырыпқа өтіп, біліміңізді одан әрі дамытыңыз."
        )
    elif last_percentage >= 60:
        st.write(
            "Қиын болған тақырыптарды қайталап, "
            "жаңа тест орындаңыз."
        )
    else:
        st.write(
            "Алдымен 📚 Сабақ бөлімінде тақырыпты оқып, "
            "содан кейін 📝 Тест тапсырыңыз."
        )
# Оқу жоспары
elif page == "📅 Жеке оқу жоспары":
    st.header("📅 Жеке оқу жоспары")

    st.write(
        "Өзіңіз туралы ақпаратты енгізіңіз. "
        "AI сізге жеке оқу жоспарын құрады."
    )

    subject = st.selectbox(
        "📚 Пәнді таңдаңыз",
        [
            "Информатика",
            "Математика",
            "Қазақ тілі",
            "Ағылшын тілі",
            "Физика"
        ],
        key="plan_subject"
    )

    level = st.selectbox(
        "🎓 Қазіргі деңгейіңіз",
        [
            "Бастапқы",
            "Орта",
            "Жоғары"
        ],
        key="plan_level"
    )

    goal = st.text_input(
        "🎯 Оқу мақсатыңыз",
        placeholder="Мысалы: Python тілін үйрену"
    )

    days = st.slider(
        "📅 Аптасына қанша күн оқисыз?",
        min_value=1,
        max_value=7,
        value=5
    )

    minutes = st.slider(
        "⏱️ Күніне қанша минут оқисыз?",
        min_value=15,
        max_value=180,
        value=60,
        step=15
    )

    duration = st.selectbox(
        "🗓️ Жоспар ұзақтығы",
        [
            "1 апта",
            "2 апта",
            "1 ай"
        ]
    )

    if st.button("🤖 AI оқу жоспарын құру"):

        if not goal:
            st.warning("Алдымен оқу мақсатыңызды жазыңыз.")

        elif not API_KEY:
            st.error("Gemini API Key табылмады.")

        else:

            with st.spinner("AI сізге жеке оқу жоспарын дайындап жатыр..."):

                try:

                    plan_prompt = f"""
Сен оқушыға арналған AI оқу жоспарлаушысысың.

Оқушының мәліметтері:

Пән: {subject}
Деңгейі: {level}
Мақсаты: {goal}
Аптасына оқу күні: {days}
Күніне оқу уақыты: {minutes} минут
Жоспар ұзақтығы: {duration}

Оқушыға түсінікті және нақты оқу жоспарын құрастыр.

Жоспарда:

1. Жалпы мақсат
2. Күтілетін нәтиже
3. Әр күнге арналған тақырып
4. Әр күнге арналған тапсырма
5. Қайталау бөлімі
6. Практикалық тапсырмалар
7. Апта соңындағы өзін-өзі тексеру

Жоспарды қазақ тілінде жаз.

Әр күнді жеке көрсет.

Оқу уақытына сәйкес тапсырмаларды шамадан тыс көп берме.
"""

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=plan_prompt
                    )

                    st.session_state.study_plan = response.text
                    save_study_plan(response.text)

                    st.success("Оқу жоспары дайын! ✅")

                except Exception as e:

                    st.error(
                        "Оқу жоспарын құру кезінде қате пайда болды."
                    )

                    st.exception(e)

    # Дайын жоспарды көрсету
    if "study_plan" in st.session_state:

        st.divider()

        st.subheader("📖 Сіздің жеке оқу жоспарыңыз")

        st.markdown(
            st.session_state.study_plan
        )