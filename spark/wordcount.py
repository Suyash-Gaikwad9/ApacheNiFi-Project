from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SimpleWordCount") \
    .master("local[*]") \
    .getOrCreate()

try:
    text_files = spark.read.text("/data/input/*")
    words = text_files.selectExpr("explode(split(value, ' ')) as word")
    word_counts = words.groupBy("word").count()

    print("\n=== WORD COUNTS ===")
    word_counts.show()
    print("===================\n")

except Exception as e:
    print(f"Error processing data: {e}")

finally:
    spark.stop()
