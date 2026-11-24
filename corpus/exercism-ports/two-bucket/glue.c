/* Host C: the upstream interface on top of the port. Not verified. */
#include "two_bucket.h"

long measure_into(long bucket_1_size, long bucket_2_size, long goal_liters, long start_bucket, long m, long out[]);

bucket_result_t measure(bucket_liters_t bucket_1_size, bucket_liters_t bucket_2_size, bucket_liters_t goal_volume,
                        bucket_id_t start_bucket)
{
   long out[4] = { 0, 0, 0, 0 };
   measure_into(bucket_1_size, bucket_2_size, goal_volume, (long)(int)start_bucket, 4, out);
   return (bucket_result_t){ .possible = out[0] != 0,
                             .move_count = (int)out[1],
                             .goal_bucket = (bucket_id_t)out[2],
                             .other_bucket_liters = (bucket_liters_t)out[3] };
}
