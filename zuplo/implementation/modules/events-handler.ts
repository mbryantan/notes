import { ZuploContext, ZuploRequest, environment } from "@zuplo/runtime";
import { createClient } from '@supabase/supabase-js';

export async function handleEvents(request: ZuploRequest, context: ZuploContext) {
  try {
    // Parse query parameters
    const url = new URL(request.url);
    const limit = Math.min(parseInt(url.searchParams.get("limit") || "10"), 100);
    const offset = parseInt(url.searchParams.get("offset") || "0");
    const startTime = url.searchParams.get("start_time");
    const endTime = url.searchParams.get("end_time");

    // Input validation
    if (isNaN(limit) || limit < 1) {
      return new Response(
        JSON.stringify({
          status: "error",
          code: 400,
          message: "Invalid limit parameter"
        }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    if (isNaN(offset) || offset < 0) {
      return new Response(
        JSON.stringify({
          status: "error",
          code: 400,
          message: "Invalid offset parameter"
        }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    // Initialize Supabase client with anon key (respects Row Level Security)
    const supabase = createClient(
      environment.SUPABASE_URL,
      environment.SUPABASE_ANON_KEY
    );

    // Build query
    let query = supabase
      .from('events')
      .select('time, event_id')
      .range(offset, offset + limit - 1);

    // Add filters if provided
    if (startTime) {
      query = query.gte('time', startTime);
    }

    if (endTime) {
      query = query.lte('time', endTime);
    }

    // Execute query
    const { data: events, error } = await query;

    if (error) {
      context.log.error("Supabase query error", { error });

      return new Response(
        JSON.stringify({
          status: "error",
          code: 400,
          message: "Error fetching data from database"
        }),
        { status: 400, headers: { "Content-Type": "application/json" } }
      );
    }

    // Format response according to requirements
    return new Response(
      JSON.stringify({
        status: "success",
        code: 200,
        data: {
          events: events
        }
      }),
      { status: 200, headers: { "Content-Type": "application/json" } }
    );
  } catch (error) {
    context.log.error("Unexpected error", { error });

    return new Response(
      JSON.stringify({
        status: "error",
        code: 500,
        message: "An unexpected error occurred"
      }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}
