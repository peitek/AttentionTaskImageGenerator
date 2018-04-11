import generate_attention_task
import generate_filler_images


def main():
    generate_filler_images.generate_calibration_image()

    for i in range(30):
        generate_filler_images.generate_decision_time_image(i)
        generate_filler_images.generate_rest_condition_image(i)
        generate_attention_task.generate_attention_task_image(i)


main()