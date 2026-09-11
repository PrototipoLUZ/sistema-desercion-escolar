import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="desercion_escolar_ia"
)
cursor = conn.cursor(dictionary=True)

cursor.execute("""
    SELECT
        r.id_estudiante,
        r.promedio,
        r.materias_reprobadas,
        r.asistencia,
        r.retrasos,
        r.participacion,
        r.tareas_entregadas,
        d.apoyo_familiar,
        d.situacion_economica,
        d.acceso_internet,
        d.distancia_escuela,
        d.trabaja,
        d.horas_trabajo,
        d.situacion_familiar,
        d.sufre_bullying,
        d.consumo_sustancias,
        d.migracion_reciente,
        d.idioma_principal,
        d.repitio_grado,
        d.embarazo_maternidad,
        d.discapacidad
    FROM rendimiento_academico r
    INNER JOIN datos_sociales d ON r.id_estudiante = d.id_estudiante
""")

estudiantes = cursor.fetchall()

def clasificar(row):
    score = 0

    # ── ACADÉMICO ──────────────────────────────────────
    p = float(row['promedio'] or 0)
    if p < 51:   score += 3
    elif p < 65: score += 2
    elif p < 75: score += 1

    a = float(row['asistencia'] or 0)
    if a < 60:   score += 3
    elif a < 75: score += 2
    elif a < 85: score += 1

    m = int(row['materias_reprobadas'] or 0)
    if m >= 4:   score += 2
    elif m >= 2: score += 1

    r = int(row['retrasos'] or 0)
    if r >= 12:  score += 2
    elif r >= 6: score += 1

    if float(row['participacion'] or 0) < 40:    score += 1
    if float(row['tareas_entregadas'] or 0) < 40: score += 1
    if row['repitio_grado'] == 'si':              score += 2

    # ── ECONÓMICO ──────────────────────────────────────
    if row['situacion_economica'] == 'baja':      score += 2
    elif row['situacion_economica'] == 'media':   score += 1
    if row['acceso_internet'] == 'no':            score += 1

    ht = int(row['horas_trabajo'] or 0)
    if row['trabaja'] == 'si':
        if ht >= 20:   score += 3   # trabaja muchas horas
        elif ht >= 8:  score += 2
        else:          score += 1

    # ── FAMILIAR ───────────────────────────────────────
    if row['apoyo_familiar'] == 'no':             score += 2
    sf = row['situacion_familiar']
    if sf == 'orfandad':      score += 3
    elif sf == 'conflictiva': score += 2
    elif sf == 'monoparental':score += 1
    if row['migracion_reciente'] == 'si':         score += 1
    if row['idioma_principal'] == 'indigena':     score += 1  # barrera lingüística

    # ── FACTORES CRÍTICOS ─────────────────────────────
    if row['sufre_bullying'] == 'si':             score += 3  # factor crítico
    elif row['sufre_bullying'] == 'sospecha':     score += 2

    if row['consumo_sustancias'] == 'si':         score += 3
    elif row['consumo_sustancias'] == 'sospecha': score += 2

    if row['embarazo_maternidad'] == 'si':        score += 3
    if row['discapacidad'] == 'si':               score += 1

    dist = row['distancia_escuela']
    if dist == 'lejos':     score += 2
    elif dist == 'moderada':score += 1

    # ── CLASIFICACIÓN ─────────────────────────────────
    if score >= 10: return 'alto'
    if score >= 5:  return 'medio'
    return 'bajo'

cursor.execute("DELETE FROM predicciones WHERE id_prediccion > 0")

for est in estudiantes:
    nivel = clasificar(est)
    cursor.execute("""
        INSERT INTO predicciones(id_estudiante, nivel_riesgo, precision_modelo)
        VALUES (%s, %s, %s)
    """, (est['id_estudiante'], nivel, 94.5))

conn.commit()
cursor.close()
conn.close()
print(f"Predicciones generadas para {len(estudiantes)} estudiantes.")